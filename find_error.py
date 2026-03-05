import os
import sys
import django
from django.template import Template, Context

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "study_buddy_project.settings")
django.setup()

with open(r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Only keep block content
start_marker = "{% block content %}"
end_marker = "{% endblock %}"
start_idx = content.find(start_marker)
end_idx = content.rfind(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Cannot find content block")
    sys.exit(1)

content_to_test = content[start_idx + len(start_marker) : end_idx]
lines = content_to_test.splitlines()

# Binary search
low = 0
high = len(lines)
ans = -1

while low <= high:
    mid = (low + high) // 2
    sub_content = "\n".join(lines[:mid])
    
    # Try to close any open tags
    if sub_content.count('{% for ') > sub_content.count('{% endfor %}'):
        sub_content += "{% endfor %}" * (sub_content.count('{% for ') - sub_content.count('{% endfor %}'))
    if sub_content.count('{% if ') > sub_content.count('{% endif %}'):
        sub_content += "{% endif %}" * (sub_content.count('{% if ') - sub_content.count('{% endif %}'))

    try:
        Template(sub_content)
        low = mid + 1
        ans = mid
    except Exception as e:
        high = mid - 1
        print(f"Error at line {mid}: {e}")

print(f"Template seems to break around line {ans+1}")
for i in range(max(0, ans - 5), min(len(lines), ans + 5)):
    print(f"{i+1}: {lines[i]}")
