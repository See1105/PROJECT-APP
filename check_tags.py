import re

with open(r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

tokens = re.findall(r'{%\s*(if|else|elif|endif|for|empty|endfor|block|endblock)\b', content)
stack = []
for i, token in enumerate(tokens):
    if token == 'if':
        stack.append(('if', i))
    elif token == 'endif':
        if not stack or stack[-1][0] != 'if':
            print(f"Error: unmatched endif at index {i}")
        else:
            stack.pop()
    elif token == 'for':
        stack.append(('for', i))
    elif token == 'endfor':
        if not stack or stack[-1][0] != 'for':
            print(f"Error: unmatched endfor at index {i}")
        else:
            stack.pop()
    elif token == 'block':
        stack.append(('block', i))
    elif token == 'endblock':
        if not stack or stack[-1][0] != 'block':
            print(f"Error: unmatched endblock at index {i}")
        else:
            stack.pop()

if stack:
    print("Unclosed tags:")
    for tag, i in stack:
        print(f" - {tag}")
else:
    print("All tags matched!")
