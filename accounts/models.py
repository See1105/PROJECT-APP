from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Profile fields
    bio = models.TextField(max_length=500, blank=True)

    points = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    preferred_language = models.CharField(max_length=20, default='English')
    theme_choice = models.CharField(max_length=20, default='dark')
    study_mode = models.CharField(max_length=20, default='Study', choices=[('Study', 'Study'), ('Quiz', 'Quiz'), ('Chat', 'Chat')])
    default_difficulty = models.CharField(max_length=20, default='Beginner', choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')])
    role = models.CharField(max_length=10, choices=[('Student', 'Student'), ('Teacher', 'Teacher')], default='Student')
    daily_study_goal = models.IntegerField(default=30, help_text="Daily study goal in minutes")
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Bootstrap icon name")
    users = models.ManyToManyField(CustomUser, related_name='badges', blank=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"
