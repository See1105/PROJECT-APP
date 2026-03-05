from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import ChatMessage, Document
from accounts.views import award_points
import time
import io
import PyPDF2

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AIChatView(LoginRequiredMixin, TemplateView):
    template_name = 'ai_buddy/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_history'] = ChatMessage.objects.filter(user=self.request.user).order_by('-created_at')[:10]
        return context

def ai_chat_api(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user_message = request.POST.get('message')
        
        try:
            # Create a system prompt for the study buddy persona
            system_prompt = f"""You are a helpful and encouraging AI Study Buddy. 
            Your goal is to help the user master topics efficiently and provide interactive, structured learning.
            
            USER PREFERENCES:
            - Current Mode: {request.user.study_mode}
            - Default Difficulty: {request.user.default_difficulty}
            
            CORE PERSONA & EXPLANATION RULES:
            1. W3Schools-Style Structure: When asked about a new topic, DO NOT explain everything at once.
               Instead, break it into a clear list of subtopics (Basic → Intermediate → Advanced). 
               Ask the user which subtopic they want to start with.
            2. When explaining a specific subtopic: Provide a step-by-step, beginner-friendly explanation with examples.
            3. Visual Aids: Use Markdown tables for comparisons. Use Mermaid.js (```mermaid graph TD ... ```) for flowcharts.
            4. Interactive Pacing: After explaining a concept, ask a quick conceptual question to check understanding before moving on.
            5. Personalization: Adjust your complexity to {request.user.default_difficulty} level by default.
            """
            
            # Fetch recent context for the chat history
            recent_chats = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:5]
            
            # Format history for Gemini (requires oldest to newest)
            gemini_history = []
            for chat in reversed(recent_chats):
                gemini_history.append({"role": "user", "parts": [chat.message]})
                gemini_history.append({"role": "model", "parts": [chat.response]})
                
            model = genai.GenerativeModel('gemini-flash-lite-latest', system_instruction=system_prompt)
            chat = model.start_chat(history=gemini_history)
            
            response = chat.send_message(user_message)
            ai_response = response.text
            
            # Save to database
            chat_obj = ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                response=ai_response
            )
            award_points(request.user, 5, "AI Explorer", "You earned 5 points for using the AI Study Buddy!")
            
            return JsonResponse({
                'status': 'success',
                'chat_id': chat_obj.id,
                'message': user_message,
                'response': ai_response
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f"Gemini API Error: {str(e)}"
            }, status=500)
            
    return JsonResponse({'status': 'error'}, status=400)

def toggle_favorite_chat(request, message_id):
    if request.method == 'POST' and request.user.is_authenticated:
        chat = get_object_or_404(ChatMessage, id=message_id, user=request.user)
        chat.is_favorite = not chat.is_favorite
        chat.save()
        return JsonResponse({'status': 'success', 'is_favorite': chat.is_favorite})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)


def auto_generate_flashcards_api(request):
    if request.method == 'POST' and request.user.is_authenticated:
        topic_text = request.POST.get('text')
        topic_name = request.POST.get('topic_name', 'Quick Flashcards')
        
        try:
            model = genai.GenerativeModel('gemini-flash-lite-latest')
            prompt = f"""Extract 5-10 atomic, high-quality Study Flashcard Q&A pairs from the following text:
            ---
            {topic_text}
            ---
            Format the response as a JSON list of objects with "front" and "back" keys.
            Example: [{"front": "What is DNA?", "back": "Deoxyribonucleic acid, the molecule that carries genetic instructions."}]
            Return ONLY the raw JSON list.
            """
            
            response = model.generate_content(prompt)
            import json
            import re
            
            # Clean response text
            raw_text = response.text.replace('```json', '').replace('```', '').strip()
            cards_data = json.loads(raw_text)
            
            from study.models import Deck, Flashcard
            deck = Deck.objects.create(
                title=f"AI: {topic_name}",
                description=f"Automatically generated from AI study session.",
                created_by=request.user
            )
            
            for card in cards_data:
                Flashcard.objects.create(
                    deck=deck,
                    front=card['front'],
                    back=card['back']
                )
            
            award_points(request.user, 20, "Flashcard Architect", "AI created a new deck for you! 20 points earned.")
            
            return JsonResponse({
                'status': 'success',
                'deck_id': deck.id,
                'card_count': len(cards_data)
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error'}, status=400)

def generate_dynamic_quiz_api(request):
    if request.method == 'POST' and request.user.is_authenticated:
        topic_name = request.POST.get('topic_name')
        difficulty = request.POST.get('difficulty', request.user.default_difficulty) # Beginner, Intermediate, Advanced
        question_count = int(request.POST.get('count', 5))
        
        try:
            model = genai.GenerativeModel('gemini-flash-lite-latest')
            prompt = f"""Generate a {difficulty} level multiple-choice quiz about '{topic_name}' with {question_count} questions.
            Format the response as a JSON object:
            {{
                "title": "{difficulty} Quiz: {topic_name}",
                "questions": [
                    {{
                        "text": "Question text here?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_index": 0,
                        "explanation": "Brief explanation of why Option A is correct."
                    }}
                ]
            }}
            Return ONLY the raw JSON object.
            """
            
            response = model.generate_content(prompt)
            import json
            import re
            
            raw_text = response.text.replace('```json', '').replace('```', '').strip()
            quiz_data = json.loads(raw_text)
                
            from study.models import Topic, Quiz, Question
            topic, _ = Topic.objects.get_or_create(name=topic_name)
            
            quiz = Quiz.objects.create(
                title=quiz_data.get('title', f"AI Quiz: {topic_name}"),
                topic=topic,
                created_by=request.user
            )
            
            for q_data in quiz_data.get('questions', []):
                options = q_data.get('options', [])
                correct_idx = q_data.get('correct_index', 0)
                # Map index to A, B, C, D
                letter_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
                correct_letter = letter_map.get(correct_idx, 'A')
                
                Question.objects.create(
                    quiz=quiz,
                    text=q_data.get('text'),
                    choice_a=options[0] if len(options) > 0 else '',
                    choice_b=options[1] if len(options) > 1 else '',
                    choice_c=options[2] if len(options) > 2 else '',
                    choice_d=options[3] if len(options) > 3 else '',
                    correct_answer=correct_letter,
                    explanation=q_data.get('explanation', '')
                )
                
            award_points(request.user, 25, "Quiz Architect", f"Generated a new {difficulty} quiz for {topic_name}!")
            
            return JsonResponse({
                'status': 'success',
                'quiz_id': quiz.id
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error'}, status=400)

def generate_study_plan_api(request):
    if request.method == 'POST' and request.user.is_authenticated:
        topic_name = request.POST.get('topic_name')
        goal_date = request.POST.get('goal_date')
        
        if not topic_name or not goal_date:
            return JsonResponse({'status': 'error', 'message': 'Topic and goal date are required.'}, status=400)
        
        try:
            model = genai.GenerativeModel('gemini-flash-lite-latest')
            prompt = f"""Create a comprehensive and personalized study plan for: {topic_name}.
            The target proficiency date is {goal_date}.
            
            Return ONLY a valid JSON object with the following exact structure:
            {{
                "overview": {{
                    "total_duration": "X weeks/days",
                    "daily_study_hours": "X hours",
                    "key_focus_areas": ["topic1", "topic2"]
                }},
                "weekly_breakdown": [
                    {{
                        "week": 1,
                        "topics": [
                            {{"subject": "Topic Name", "hours_per_day": "X hours", "study_method": "e.g. flashcards"}}
                        ],
                        "milestone": "Goal for the week"
                    }}
                ],
                "daily_routine": {{
                    "morning": "Task/Topic",
                    "afternoon": "Task/Topic",
                    "evening": "Task/Topic",
                    "breaks": "Duration & timing"
                }},
                "action_items": [
                    {{"task": "Specific task like 'Revise Chapter 3'", "is_milestone": true}},
                    {{"task": "Solve 20 SQL queries", "is_milestone": true}}
                ],
                "tracking": {{
                    "frequency": "Daily",
                    "adjust_condition": "e.g., falling behind"
                }}
            }}
            """
            
            response = model.generate_content(prompt)
            import json
            import re
            
            # Clean response to ensure it's just JSON
            raw_text = response.text.replace('```json', '').replace('```', '').strip()
            plan_data = json.loads(raw_text)
                
            from study.models import Topic, StudyPlan, Milestone
            topic, _ = Topic.objects.get_or_create(name=topic_name)
            
            study_plan = StudyPlan.objects.create(
                user=request.user,
                topic=topic,
                goal_date=goal_date,
                progress=0,
                plan_details=plan_data
            )
            
            # Create Milestones from action items marked as milestones
            for item in plan_data.get('action_items', []):
                if item.get('is_milestone', True):
                    Milestone.objects.create(
                        plan=study_plan,
                        task_name=item.get('task', 'Untitled Task')
                    )

            award_points(request.user, 30, "Strategic Planner", f"New study plan created for {topic_name}!")
            
            return JsonResponse({
                'status': 'success',
                'plan_id': study_plan.id,
                'message': f'Plan for {topic_name} generated successfully!'
            })
            
        except Exception as e:
            print(f"Study Plan Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'ai_buddy/document_list.html'
    context_object_name = 'documents'

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

class DocumentUploadView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['title', 'file']
    template_name = 'ai_buddy/document_form.html'
    success_url = reverse_lazy('document_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        
        # Real AI Summarization
        file = self.request.FILES.get('file')
        if file:
            try:
                content = ""
                file_ext = file.name.split('.')[-1].lower()
                
                if file_ext == 'pdf':
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                    for page in pdf_reader.pages:
                        extracted = page.extract_text()
                        if extracted: content += extracted + "\n"
                else:
                    content = file.read().decode('utf-8', errors='ignore')

                if content.strip():
                    model = genai.GenerativeModel('gemini-flash-lite-latest')
                    prompt = f"""Summarize the following study material using this exact structure:
                    
                    1. Overview:
                       - Purpose and scope of the document in 2–3 sentences.
                    
                    2. Key Points (Detailed):
                       - [Detailed explanations of all major points]
                    
                    3. Important Terms / Definitions:
                       - [Term] — [Simple explanation]
                    
                    4. Actionable Insights / Study Notes:
                       - [Key takeaways and exam relevance]
                    
                    5. Conversational Recap:
                       "So basically, this document is saying that..."
                       (Provide a short, friendly explanation in plain language, 5–7 sentences)
                    
                    Material:
                    {content[:15000]}
                    """
                    response = model.generate_content(prompt)
                    form.instance.summary = response.text
                else:
                    form.instance.summary = "The document appears to be empty or unreadable."
            except Exception as e:
                print(f"Summarization Error: {str(e)}")
                form.instance.summary = "AI was unable to process this file, but you can still access it below."
        
        response = super().form_valid(form)
        award_points(self.request.user, 30, "Knowledge Weaver", "AI summarized your document! 30 points earned.")
        return response
