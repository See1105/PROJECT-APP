from django.db import models
from django.conf import settings

class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, default='General')
    icon = models.CharField(max_length=50, default='book') # Bootstrap icon name
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Deck(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    topic = models.ForeignKey(Topic, related_name='decks', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Flashcard(models.Model):
    deck = models.ForeignKey(Deck, related_name='cards', on_delete=models.CASCADE)
    front = models.TextField()
    back = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card for {self.deck.title}"

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    topic = models.ForeignKey(Topic, related_name='quizzes', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    choice_a = models.CharField(max_length=255)
    choice_b = models.CharField(max_length=255)
    choice_c = models.CharField(max_length=255)
    choice_d = models.CharField(max_length=255)
    CORRECT_CHOICES = [
        ('A', 'Choice A'),
        ('B', 'Choice B'),
        ('C', 'Choice C'),
        ('D', 'Choice D'),
    ]
    correct_answer = models.CharField(max_length=1, choices=CORRECT_CHOICES)
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Question in {self.quiz.title}"

class QuizSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}/{self.total_questions})"

class WeakTopic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weak_topics')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    difficulty_score = models.FloatField(default=0.0) # 0 to 1 scale
    last_attempt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user.username}'s weakness: {self.topic.name}"

class StudyPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_plans')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    goal_date = models.DateField()
    progress = models.IntegerField(default=0) # 0 to 100 percentage
    plan_details = models.JSONField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Study plan for {self.user.username}: {self.topic.name}"

class Milestone(models.Model):
    plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name='milestones')
    task_name = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Milestone: {self.task_name} (Plan: {self.plan.id})"
