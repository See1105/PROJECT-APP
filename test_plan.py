import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_buddy_project.settings')
django.setup()

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

topic_name = "Modern Physics"
goal_date = "2026-06-30"

model = genai.GenerativeModel('gemini-2.5-flash')
prompt = f"""Create a highly effective 3-step study plan for: {topic_name}.
The goal is to be proficient by {goal_date}.

Return ONLY a valid JSON object with this exact structure:
{{
    "topic": "{topic_name}",
    "milestones": [
        {{"title": "Breakdown/Phase 1", "description": "Short explanation..."}},
        {{"title": "Phase 2", "description": "..."}},
        {{"title": "Final Review/Phase 3", "description": "..."}}
    ]
}}
"""

with open('test_plan_out.txt', 'w') as f:
    try:
        response = model.generate_content(prompt)
        f.write("RAW RESPONSE:\n")
        f.write(response.text + "\n")

        import json
        import re

        content = response.text
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            f.write("MATCHED JSON!\n")
            try:
                plan_data = json.loads(json_match.group())
                f.write(f"PARSED: {plan_data}\n")
            except Exception as e:
                f.write(f"JSON Error: {str(e)}\n")
        else:
            f.write("NO MATCH\n")
    except Exception as e:
        f.write(f"Generation Error: {str(e)}\n")

print("Done")
