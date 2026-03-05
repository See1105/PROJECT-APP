from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views import View
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Badge, Notification
from study.models import Topic, WeakTopic
from django.db.models import Count, Sum, Avg
from django.views.generic.edit import UpdateView

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        return ['dashboard.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Personalized Context
        context['notifications'] = Notification.objects.filter(user=user, is_read=False).order_by('-created_at')[:5]
        context['topics'] = Topic.objects.all() # Or filtered by user's active topics
        context['weak_topics'] = WeakTopic.objects.filter(user=user).order_by('-difficulty_score')[:3]
        
        # Stats Calculation
        context['total_decks'] = user.deck_set.count()
        context['total_quizzes_taken'] = user.quizsubmission_set.count()
        context['avg_score'] = user.quizsubmission_set.aggregate(Avg('score'))['score__avg'] or 0
        
        # History (Mix of quizzes and chats)
        from study.models import QuizSubmission
        from ai_buddy.models import ChatMessage
        # Recent History (Mix of quizzes and chats)
        recent_quizzes = list(QuizSubmission.objects.filter(user=user).select_related('quiz').order_by('-submitted_at')[:3])
        recent_chats = list(ChatMessage.objects.filter(user=user).order_by('-created_at')[:3])
        
        # Simple sorting to interleave history
        history = []
        for q in recent_quizzes:
            history.append({'type': 'quiz', 'title': q.quiz.title, 'date': q.submitted_at, 'score': q.score})
        for c in recent_chats:
            history.append({'type': 'chat', 'title': c.message[:30] + '...', 'date': c.created_at})
            
        history.sort(key=lambda x: x['date'], reverse=True)
        context['history'] = history[:5]
        context['starred_chats'] = ChatMessage.objects.filter(user=user, is_favorite=True).order_by('-created_at')[:5]
        
        return context

class SettingsView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['username', 'email', 'avatar', 'preferred_language', 'theme_choice', 'bio', 'daily_study_goal']
    template_name = 'accounts/settings.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user

class DeleteAccountView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')

def award_points(user, amount, title, message):
    user.points += amount
    user.save()
    Notification.objects.create(user=user, title=title, message=message)
