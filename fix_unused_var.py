import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'autoRt.anchoredPosition = new Vector2(-310, -10);' in line:
        lines[i] = '            autoRt.anchoredPosition = new Vector2(-(10 + btnW * 2 + btnSpacing * 2), -10);\n'
    elif 'skipRt.anchoredPosition = new Vector2(-160, -10);' in line:
        lines[i] = '            skipRt.anchoredPosition = new Vector2(-(10 + btnW + btnSpacing), -10);\n'
    elif 'logRt.anchoredPosition = new Vector2(-10, -10);' in line:
        lines[i] = '            logRt.anchoredPosition = new Vector2(-10, -10);\n'

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("HalloweenUIBuilder updated to use btnW and btnSpacing")
