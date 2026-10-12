import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'titleRt.anchoredPosition = new Vector2(0, 230);' in line:
        lines[i] = line.replace('230', '300')

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Updated logo to 300.")
