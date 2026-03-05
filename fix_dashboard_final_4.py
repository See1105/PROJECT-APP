import os
import re

path = r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Unsplit {{ ... }}
pattern_curly = r"\{\{\s*(.*?)\s*\}\}"
content = re.sub(r"\{\{\s*\n\s*", "{{ ", content)
content = re.sub(r"\s*\n\s*\}\}", " }}", content)

# Unsplit {% ... %}
# This is trickier because some tags like 'block' should stay on one line anyway.
# Let's target the specific welcome back one.
content = content.replace("{{ user.username\n                            }}", "{{ user.username }}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed unsplit tags")
