import re

with open(r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    tags = re.findall(r'{%\s*(.*?)\s*%}', line)
    for tag in tags:
        print(f"L{i}: {{% {tag} %}}")
