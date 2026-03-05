
import os

def fix_dashboard():
    path = r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix split {{ user.username }}
    content = content.replace('{{ user.username\n                            }}', '{{ user.username }}')
    
    # Fix split {{ task.plan.topic.name }}
    content = content.replace('{{ task.plan.topic.name\n                                    }}', '{{ task.plan.topic.name }}')
    
    # Fix spacing in if tags
    content = content.replace("user.default_difficulty=='Beginner'", "user.default_difficulty == 'Beginner'")
    content = content.replace("user.default_difficulty=='Intermediate'", "user.default_difficulty == 'Intermediate'")
    content = content.replace("user.default_difficulty=='Advanced'", "user.default_difficulty == 'Advanced'")
    
    # Fix potential block syntax issues
    # Ensure no split {% if ... %} tags if any left
    import re
    content = re.sub(r'{%\s*if\s+user\.default_difficulty\s*==\s*\'Intermediate\'\s*%}\s*{%\s*endif\s*%}', 
                     r"{% if user.default_difficulty == 'Intermediate' %}selected{% endif %}", content)

    # I noticed a weird bit in my previous replace call:
    # <option value="Intermediate" {% if user.default_difficulty=='Intermediate' %}{%
    #     endif %}>
    # Wait, the 'selected' was missing or something was wrong.
    
    # Let's just fix the whole block for difficulty options
    difficulty_block = """                        <select class="form-select bg-dark text-white border-white-10" id="quizDifficulty">
                            <option value="Beginner" {% if user.default_difficulty == 'Beginner' %}selected{% endif %}>
                                Beginner
                            </option>
                            <option value="Intermediate" {% if user.default_difficulty == 'Intermediate' %}selected{% endif %}>
                                Intermediate
                            </option>
                            <option value="Advanced" {% if user.default_difficulty == 'Advanced' %}selected{% endif %}>
                                Advanced
                            </option>
                        </select>"""
    
    # Find the current block and replace it
    # We'll use a regex to find the select tag and everything inside it
    content = re.sub(r'<select class="form-select bg-dark text-white border-white-10" id="quizDifficulty">.*?</select>', 
                     difficulty_block, content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Dashboard fixed.")

if __name__ == "__main__":
    fix_dashboard()
