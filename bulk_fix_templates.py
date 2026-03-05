
import os
import re

def fix_all_templates():
    folders = ['templates', 'accounts', 'study', 'ai_buddy', 'collaboration']
    for folder in folders:
        if not os.path.exists(folder): continue
        for root, dirs, files in os.walk(folder):
            if 'venv' in root: continue
            for file in files:
                if file.endswith('.html'):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Fix spacing in if/elif tags: {% if x==y %} -> {% if x == y %}
                    # This regex handles == and !=
                    content = re.sub(r'{%\s*(if|elif)\s+([^%]+?)\s*%}', 
                                     lambda m: '{% ' + m.group(1) + ' ' + m.group(2).replace('==', ' == ').replace('!=', ' != ').replace('  ', ' ') + ' %}', 
                                     content)
                    
                    # Fix split variables {{ \n }}
                    content = re.sub(r'({{[^}]*)\n\s*([^}]*}})', r'\1 \2', content)
                    
                    # Fix split tags {% \n %}
                    content = re.sub(r'({%[^%]*)\n\s*([^%]*%})', r'\1 \2', content)
                    
                    # Double check common ones that might still be split
                    content = content.replace('{{ task.plan.topic.name\n                                    }}', '{{ task.plan.topic.name }}')
                    content = content.replace('{{ user.username\n                            }}', '{{ user.username }}')

                    if content != original_content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"FIXED: {path}")

if __name__ == "__main__":
    fix_all_templates()
