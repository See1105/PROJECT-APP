from django.urls import path
from .views import (
    AIChatView, ai_chat_api, toggle_favorite_chat,
    DocumentListView, DocumentUploadView,
    auto_generate_flashcards_api, generate_study_plan_api,
    generate_dynamic_quiz_api
)

urlpatterns = [
    path('chat/', AIChatView.as_view(), name='ai_chat'),
    path('api/chat/', ai_chat_api, name='ai_chat_api'),
    path('api/chat/<int:message_id>/favorite/', toggle_favorite_chat, name='toggle_favorite_chat'),
    path('api/generate-flashcards/', auto_generate_flashcards_api, name='auto_generate_flashcards_api'),
    path('api/generate-study-plan/', generate_study_plan_api, name='generate_study_plan_api'),
    path('api/generate-dynamic-quiz/', generate_dynamic_quiz_api, name='generate_dynamic_quiz_api'),
    path('summarizer/', DocumentListView.as_view(), name='document_list'),
    path('summarizer/upload/', DocumentUploadView.as_view(), name='document_upload'),
]
