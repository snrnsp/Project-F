import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'titleRt.anchoredPosition = new Vector2(0, 230);' in line:
        lines[i] = line.replace('230', '270')
    if 'float startY = 40f; // Lowered to give breathing room from the logo' in line:
        lines[i] = '            float startY = 90f; // Shifted slightly up\n'

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Updated logo and buttons Y position.")
