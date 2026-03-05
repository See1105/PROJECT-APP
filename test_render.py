import os
import sys
import django
from django.template.loader import render_to_string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "study_buddy_project.settings")
django.setup()

try:
    class MockUser:
        is_authenticated = True
        username = "testuser"
        def __str__(self): return self.username
    
    context = {'request': type('MockRequest', (object,), {'user': MockUser()})}
    html = render_to_string('dashboard.html', context)
    print("TEMPLATE_RENDER_SUCCESS")
except Exception as e:
    import traceback
    with open('error.txt', 'w', encoding='utf-8') as f:
        traceback.print_exc(file=f)
