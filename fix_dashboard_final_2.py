import os

path = r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("user.default_difficulty=='Beginner'", "user.default_difficulty == 'Beginner'")
content = content.replace("user.default_difficulty=='Intermediate'", "user.default_difficulty == 'Intermediate'")
content = content.replace("user.default_difficulty=='Advanced'", "user.default_difficulty == 'Advanced'")

# Also fix the Intermediate spacing issue if it exists
content = content.replace("{% if user.default_difficulty=='Intermediate' %}selected{%\n                                endif %}", "{% if user.default_difficulty == 'Intermediate' %}selected{% endif %}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
