import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'float yPos = -120f;' in line:
        lines[i] = '            float yPos = -80f;\n'
    if 'panelRt.sizeDelta = new Vector2(700, 1000);' in line:
        lines[i] = '            panelRt.sizeDelta = new Vector2(700, 750);\n' # Reduced from 1000 to 750
    if 'yPos -= 105;' in line:
        lines[i] = line.replace('yPos -= 105;', 'yPos -= 85;')
    if 'yPos -= 70;' in line:
        lines[i] = line.replace('yPos -= 70;', 'yPos -= 60;')

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Compressed Settings UI spacing.")
