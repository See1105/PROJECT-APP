from django.urls import path
from . import views

urlpatterns = [
    path('',               views.video_buddy_home, name='video_buddy'),
    path('search/',        views.search_videos,    name='video_search'),
    path('favourites/save/',        views.save_favourite,   name='save_favourite'),
    path('favourites/<int:pk>/edit/',   views.edit_favourite,   name='edit_favourite'),
    path('favourites/<int:pk>/delete/', views.delete_favourite, name='delete_favourite'),
]
