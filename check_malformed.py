import re

with open(r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    openings = line.count('{%')
    closings = line.count('%}')
    if openings != closings:
        print(f"Mismatch on line {i}: {openings} openings, {closings} closings")
        print(f"Content: {line.strip()}")
