import os

path = r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the specific broken Intermediate option
# It looks like: {% if user.default_difficulty == 'Intermediate' %}selected{% \n endif %}
import re
pattern = r"{% if user\.default_difficulty == 'Intermediate' %}selected{%\s*\n\s*endif %}"
content = re.sub(pattern, "{% if user.default_difficulty == 'Intermediate' %}selected{% endif %}", content)

# Also fix the other potential ones
pattern2 = r"{% if user\.default_difficulty=='Intermediate' %}selected{%\s*\n\s*endif %}"
content = re.sub(pattern2, "{% if user.default_difficulty == 'Intermediate' %}selected{% endif %}", content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed")
