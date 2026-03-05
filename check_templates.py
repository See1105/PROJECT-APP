
import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_buddy_project.settings')
django.setup()

from django.template.loader import render_to_string
from accounts.models import CustomUser
from django.template import TemplateDoesNotExist
from django.forms.models import modelform_factory

def check_all_templates():
    user = CustomUser.objects.first()
    
    # Create a form for the templates that need one
    from accounts.views import SettingsView
    SettingsForm = modelform_factory(CustomUser, fields=SettingsView.fields)
    settings_form = SettingsForm(instance=user)
    
    templates_to_check = [
        ('dashboard.html', {'user': user, 'notifications': [], 'topics': [], 'study_plans': [], 'weak_topics': [], 'upcoming_tasks': [], 'history': []}),
        ('home.html', {'user': user}),
        ('base.html', {'user': user}),
        ('accounts/login.html', {'form': None}),
        ('accounts/signup.html', {'form': None}),
        ('accounts/settings.html', {'user': user, 'form': settings_form}),
        ('study/deck_list.html', {'user': user, 'decks': []}),
        ('study/quiz_list.html', {'user': user, 'quizzes': []}),
    ]
    
    found_errors = False
    for t, ctx in templates_to_check:
        try:
            render_to_string(t, ctx)
            print(f"OK: {t}")
        except TemplateDoesNotExist:
            print(f"SKIP: {t} (not found)")
        except Exception as e:
            print(f"ERROR in {t}: {str(e)}")
            found_errors = True
            
    if not found_errors:
        print("All core templates rendered successfully.")

if __name__ == "__main__":
    check_all_templates()
