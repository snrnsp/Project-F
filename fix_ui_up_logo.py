import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'titleRt.anchoredPosition = new Vector2(0, 270);' in line:
        lines[i] = '        titleRt.anchoredPosition = new Vector2(0, 300);\n'

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Updated logo to 300.")
