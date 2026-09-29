import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'titleRt.anchoredPosition = new Vector2(' in line:
        lines[i] = '        titleRt.anchoredPosition = new Vector2(-60, 320);\n'
    elif 'titleRt.sizeDelta = new Vector2(' in line:
        lines[i] = '        titleRt.sizeDelta = new Vector2(1000, 416);\n'

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("HalloweenUIBuilder updated to fix logo size and position")
