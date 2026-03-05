import re

with open(r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

if_stack = []

for i, line in enumerate(lines, 1):
    # Find all if/endif tags on the line
    tags = re.findall(r'{%\s*(if|endif|elif|else)\s*.*?%}', line)
    for tag in tags:
        if tag == 'if':
            if_stack.append(i)
        elif tag == 'endif':
            if if_stack:
                if_stack.pop()
            else:
                print(f"Error: endif without if on line {i}")

if if_stack:
    for line_num in if_stack:
        print(f"Error: Unclosed if started on line {line_num}: {lines[line_num-1].strip()}")
else:
    print("Tags balanced according to this simple trace.")
