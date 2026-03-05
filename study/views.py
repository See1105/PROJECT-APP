from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Deck, Flashcard, Quiz, Question, QuizSubmission, Topic, WeakTopic, StudyPlan, Milestone
from accounts.views import award_points
from accounts.models import Notification
import google.generativeai as genai
import os

# --- Flashcard Views ---
class DeckListView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = 'study/deck_list.html'
    context_object_name = 'decks'

    def get_queryset(self):
        return Deck.objects.filter(created_by=self.request.user)

class DeckCreateView(LoginRequiredMixin, CreateView):
    model = Deck
    fields = ['title', 'description']
    template_name = 'study/deck_form.html'
    success_url = reverse_lazy('deck_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        award_points(self.request.user, 20, "Deck Creator", "You earned 20 points for creating a new study deck!")
        return response

class DeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = 'study/deck_detail.html'
    context_object_name = 'deck'

# --- Quiz Views ---
class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'study/quiz_list.html'
    context_object_name = 'quizzes'

class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'study/quiz_detail.html'
    context_object_name = 'quiz'

from django.views import View
from django.http import JsonResponse
import json

class QuizSubmitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        try:
            data = json.loads(request.body)
            user_answers = data.get('answers', {}) # {question_id: selected_option_index}
            
            correct_count = 0
            questions = quiz.questions.all()
            total_questions = questions.count()
            
            results = []
            for q in questions:
                # Map 0,1,2,3 from frontend to A,B,C,D
                letter_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
                user_letter = letter_map.get(int(user_answers.get(str(q.id), -1)), '')
                
                is_correct = (user_letter == q.correct_answer)
                if is_correct:
                    correct_count += 1
                
                results.append({
                    'id': q.id,
                    'is_correct': is_correct,
                    'correct_answer': q.correct_answer,
                    'explanation': q.explanation or "No explanation available."
                })
            
            score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
            
            # Save Submission
            submission = QuizSubmission.objects.create(
                user=request.user,
                quiz=quiz,
                score=int(score_percentage),
                total_questions=total_questions
            )
            
            # Adaptive Logic: Update WeakTopic
            if quiz.topic:
                weak_topic, created = WeakTopic.objects.get_or_create(
                    user=request.user,
                    topic=quiz.topic
                )
                # Increase difficulty score if performance is poor, decrease if good
                # Score 0-1 range. Lower quiz score = higher difficulty score.
                performance_ratio = correct_count / total_questions if total_questions > 0 else 1
                new_score = 1.0 - performance_ratio
                
                # Smooth update (moving average style)
                weak_topic.difficulty_score = (weak_topic.difficulty_score * 0.4) + (new_score * 0.6)
                weak_topic.save()
            
            # Generate AI Analysis if they missed something
            ai_analysis = ""
            if correct_count < total_questions:
                try:
                    # Configure API Key if needed, but assuming it's done in settings or env
                    analysis_model = genai.GenerativeModel('gemini-2.5-flash')
                    analysis_prompt = f"""The user just finished a quiz on '{quiz.topic.name if quiz.topic else quiz.title}'.
                    Score: {correct_count}/{total_questions} ({score_percentage}%).
                    Provide a single, encouraging paragraph (max 3 sentences) summarizing their performance and suggesting specific areas for improvement based on the score.
                    """
                    analysis_response = analysis_model.generate_content(analysis_prompt)
                    ai_analysis = analysis_response.text
                except Exception as e:
                    ai_analysis = "Great effort! Keep practicing to master this topic."
            else:
                ai_analysis = "Perfect score! You've mastered this topic. Ready for the next challenge?"

            # Award Points
            award_points(request.user, 10 + (correct_count * 2), "Quiz Master", f"Completed {quiz.title}!")
            
            return JsonResponse({
                'status': 'success',
                'score': score_percentage,
                'correct': correct_count,
                'total': total_questions,
                'results': results,
                'ai_analysis': ai_analysis
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class CompleteMilestoneView(LoginRequiredMixin, View):
    def post(self, request, pk):
        from .models import Milestone
        milestone = get_object_or_404(Milestone, pk=pk, plan__user=request.user)
        
        milestone.is_completed = True
        milestone.save()
        
        Notification.objects.create(
            user=request.user,
            title="Milestone Completed!",
            message=f"You've completed: {milestone.task_name}"
        )
        
        plan = milestone.plan
        total = plan.milestones.count()
        completed = plan.milestones.filter(is_completed=True).count()
        
        if total > 0:
            plan.progress = int((completed / total) * 100)
            
            if completed == total:
                plan.is_completed = True
                award_points(request.user, 50, "Goal Crusher", f"Completed study plan for {plan.topic.name}!")
                Notification.objects.create(
                    user=request.user,
                    title="Goal Reached! 🚀",
                    message=f"Congratulations! You've finished your study plan for {plan.topic.name}."
                )
            plan.save()
            
        return JsonResponse({
            'status': 'success',
            'progress': plan.progress,
            'plan_completed': plan.is_completed
        })

class StudyPlannerView(LoginRequiredMixin, ListView):
    model = StudyPlan
    template_name = 'study/study_planner.html'
    context_object_name = 'study_plans'

    def get_queryset(self):
        return StudyPlan.objects.filter(user=self.request.user).order_by('-created_at')

class StudyHistoryView(LoginRequiredMixin, ListView):
    model = QuizSubmission
    template_name = 'study/study_history.html'
    context_object_name = 'quiz_submissions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_milestones'] = Milestone.objects.filter(plan__user=self.request.user, is_completed=True).order_by('-created_at')
        context['completed_plans'] = StudyPlan.objects.filter(user=self.request.user, is_completed=True).order_by('-created_at')
        return context

    def get_queryset(self):
        return QuizSubmission.objects.filter(user=self.request.user).order_by('-submitted_at')
