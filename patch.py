import os
import re

file_path = "templates/dashboard.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("user.default_difficulty=='Beginner'", "user.default_difficulty == 'Beginner'")
content = content.replace("user.default_difficulty=='Intermediate'", "user.default_difficulty == 'Intermediate'")
content = content.replace("user.default_difficulty=='Advanced'", "user.default_difficulty == 'Advanced'")

# Fix split endif tags
content = re.sub(r'selected\{%\s*endif\s*%\}', 'selected{% endif %}', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patch applied for split endif tags.")
