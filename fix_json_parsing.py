import os
import re

path = r'c:\Users\sahis\pbl\New folder\project app\ai_buddy\views.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# flashcards
pattern1 = r"""            # Clean response text in case AI adds markdown code blocks
            json_match = re\.search\(r'\\\[\.\*\\\]', response\.text, re\.DOTALL\)
            if json_match:
                cards_data = json\.loads\(json_match\.group\(\)\)
            else:
                cards_data = json\.loads\(response\.text\)"""
replacement1 = """            # Clean response text
            raw_text = response.text.replace('```json', '').replace('```', '').strip()
            cards_data = json.loads(raw_text)"""
content = re.sub(pattern1, replacement1, content)
if "cards_data = json.loads(raw_text)" not in content:
    print("Warning: pattern1 not replaced")

# quiz
pattern2 = r"""            json_match = re\.search\(r'\\\{\.\*\\\}', response\.text, re\.DOTALL\)
            if json_match:
                quiz_data = json\.loads\(json_match\.group\(\)\)
            else:
                quiz_data = json\.loads\(response\.text\)"""
replacement2 = """            raw_text = response.text.replace('```json', '').replace('```', '').strip()
            quiz_data = json.loads(raw_text)"""
content = re.sub(pattern2, replacement2, content)
if "quiz_data = json.loads(raw_text)" not in content:
    print("Warning: pattern2 not replaced")

# plan
pattern3 = r"""            # Clean response to ensure it's just JSON
            content = response\.text
            json_match = re\.search\(r'\\\{\.\*\\\}', content, re\.DOTALL\)
            if json_match:
                plan_data = json\.loads\(json_match\.group\(\)\)
            else:
                plan_data = json\.loads\(content\)"""
replacement3 = """            # Clean response to ensure it's just JSON
            raw_text = response.text.replace('```json', '').replace('```', '').strip()
            plan_data = json.loads(raw_text)"""
content = re.sub(pattern3, replacement3, content)
if "plan_data = json.loads(raw_text)" not in content:
    print("Warning: pattern3 not replaced")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
