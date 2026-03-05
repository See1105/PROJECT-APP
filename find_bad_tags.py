
import os
import re

def find_malformed_tags(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Find {% if ... %} tags
                    tags = re.findall(r'{%\s*if\s+(.*?)\s*%}', content)
                    for tag in tags:
                        if '==' in tag and ' == ' not in tag:
                            print(f"Malformed tag in {path}: {{% if {tag} %}}")
                        if '!=' in tag and ' != ' not in tag:
                            print(f"Malformed tag in {path}: {{% if {tag} %}}")
                    
                    # Find split tags
                    # This is harder with regex, but we can look for tags that span multiple lines
                    split_tags = re.findall(r'{%\s*.+?\n.+?%}', content, re.MULTILINE)
                    for tag in split_tags:
                        print(f"Split tag in {path}:\n{tag}")

if __name__ == "__main__":
    find_malformed_tags('templates')
    find_malformed_tags('accounts/templates')
    find_malformed_tags('study/templates')
    find_malformed_tags('ai_buddy/templates')
