import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'titleRt.anchoredPosition = new Vector2(' in line:
        lines[i] = '        titleRt.anchoredPosition = new Vector2(180, 320);\n'
    elif 'titleRt.sizeDelta = new Vector2(' in line:
        lines[i] = '        titleRt.sizeDelta = new Vector2(2000, 833);\n'

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("HalloweenUIBuilder updated for centered and enlarged logo")
