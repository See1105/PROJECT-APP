path = r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Force replacement of common issues
new_content = content.replace("default_difficulty=='Beginner'", "default_difficulty == 'Beginner'")
new_content = new_content.replace("default_difficulty=='Intermediate'", "default_difficulty == 'Intermediate'")
new_content = new_content.replace("default_difficulty=='Advanced'", "default_difficulty == 'Advanced'")

# Additional fix: check for the split tag specifically
new_content = new_content.replace(
    'default_difficulty == \'Intermediate\' %}selected{%',
    'default_difficulty == \'Intermediate\' %}selected{% endif %}'
)
# Ensure we don't have double endifs
new_content = new_content.replace('endif %}\n                                endif %}', 'endif %}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Replacement complete. Checking lines...")
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[440:470], 441):
        if 'default_difficulty' in line:
            print(f"{i}: {line.strip()}")
