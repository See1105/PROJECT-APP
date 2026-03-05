from django.urls import path
from .views import (
    DeckListView, DeckCreateView, DeckDetailView,
    QuizListView, QuizDetailView, QuizSubmitView,
    CompleteMilestoneView, StudyHistoryView, StudyPlannerView
)

urlpatterns = [
    # Flashcards
    path('decks/', DeckListView.as_view(), name='deck_list'),
    path('decks/create/', DeckCreateView.as_view(), name='deck_create'),
    path('decks/<int:pk>/', DeckDetailView.as_view(), name='deck_detail'),

    # Quizzes
    path('quizzes/', QuizListView.as_view(), name='quiz_list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quizzes/<int:pk>/submit/', QuizSubmitView.as_view(), name='quiz_submit'),
    
    # Study Plans
    path('planner/', StudyPlannerView.as_view(), name='study_planner'),
    path('milestones/<int:pk>/complete/', CompleteMilestoneView.as_view(), name='complete_milestone'),
    path('history/', StudyHistoryView.as_view(), name='study_history'),
]
