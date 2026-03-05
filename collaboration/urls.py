from django.urls import path
from .views import GroupListView, GroupCreateView, GroupDetailView

urlpatterns = [
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create/', GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group_detail'),
]
