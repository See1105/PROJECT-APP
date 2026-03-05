with open(r'c:\Users\sahis\pbl\New folder\project app\templates\dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

if_count = content.count('{% if ')
elif_count = content.count('{% elif ')
else_count = content.count('{% else ')
endif_count = content.count('{% endif %}')

print(f"If: {if_count}")
print(f"Elif: {elif_count}")
print(f"Else: {else_count}")
print(f"Endif: {endif_count}")

# Check lines around 450-465
lines = content.splitlines()
for i, line in enumerate(lines[440:470], 441):
    print(f"{i}: {line}")
