
import os
import re

def check_files():
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
                        
                        # Find tags like {% if x==y %}
                        bad_if = re.findall(r'{%\s*(?:if|elif)\s+[^%]*[^ ]==[^ ][^%]*\s*%}', content)
                        for tag in bad_if:
                            print(f"BAD SPACING: {path}: {tag}")
                            
                        # Find split tags {% \n %}
                        # Exclude legitimate multi-line blocks like {% block %} ... {% endblock %}
                        # We want to find single tags that are split
                        split_tag = re.findall(r'{%[^{%]*\n[^{%]*%}', content)
                        for tag in split_tag:
                            if 'target_dir' in tag or 'block' in tag: continue # some tags might be okay? actually no, {% url %} or {% if %} shouldn't be split usually
                            print(f"SPLIT TAG: {path}: {tag!r}")
                            
                        # Find split variables {{ \n }}
                        split_var = re.findall(r'{{[^{{]*\n[^{{]*}}', content)
                        for var in split_var:
                            print(f"SPLIT VAR: {path}: {var!r}")

if __name__ == "__main__":
    check_files()
