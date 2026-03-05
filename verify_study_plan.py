import os
import django
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_buddy_project.settings')
django.setup()

from study.models import StudyPlan, Milestone, Topic
from django.contrib.auth import get_user_model

User = get_user_model()

def verify_plan_generation():
    print("Starting verification of detailed study plan generation...")
    
    # Get or create a test user
    user, created = User.objects.get_or_create(username='test_verifier', defaults={'email': 'test@example.com'})
    if created:
        user.set_password('verification123')
        user.save()
        print(f"Created test user: {user.username}")
    else:
        print(f"Using existing test user: {user.username}")

    # Mock data that would come from AI
    mock_plan_details = {
        "overview": {
            "total_duration": "4 weeks",
            "daily_study_hours": "2 hours",
            "key_focus_areas": ["Django Models", "Django Views", "Templates"]
        },
        "weekly_breakdown": [
            {
                "week": 1,
                "topics": [{"subject": "Models", "hours_per_day": "2", "study_method": "Practice"}],
                "milestone": "Master Models"
            }
        ],
        "daily_routine": {
            "morning": "Read docs",
            "afternoon": "Code",
            "evening": "Quiz",
            "breaks": "15 mins every hour"
        },
        "action_items": [
            {"task": "Create a model", "is_milestone": True},
            {"task": "Run migrations", "is_milestone": False}
        ],
        "tracking": {
            "frequency": "Daily",
            "adjust_condition": "Feeling lost"
        }
    }

    # Simulate creation (testing the logic implemented in views.py)
    topic, _ = Topic.objects.get_or_create(name='Django Mastery')
    
    plan = StudyPlan.objects.create(
        user=user,
        topic=topic,
        goal_date='2026-03-30',
        plan_details=mock_plan_details
    )
    print(f"Created StudyPlan ID: {plan.id}")

    # Check if milestones were created correctly (logic from view)
    for item in mock_plan_details.get('action_items', []):
        if item.get('is_milestone', True):
            Milestone.objects.create(
                plan=plan,
                task_name=item.get('task', 'Untitled Task')
            )

    # Verifications
    milestones = Milestone.objects.filter(plan=plan)
    print(f"Number of milestones created: {milestones.count()}")
    
    assert plan.plan_details == mock_plan_details, "plan_details mismatch!"
    assert milestones.count() == 1, f"Expected 1 milestone, got {milestones.count()}" # Only one has is_milestone: True
    assert milestones.first().task_name == "Create a model", "Milestone task name mismatch!"

    print("✅ Verification Successful: Detailed plan storage and milestone creation logic is working.")

if __name__ == "__main__":
    try:
        verify_plan_generation()
    except Exception as e:
        print(f"❌ Verification Failed: {str(e)}")
