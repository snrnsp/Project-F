import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # 1. Update logo size and pos
    if 'titleRt.anchoredPosition = new Vector2(-60, 230);' in line:
        lines[i] = '        titleRt.anchoredPosition = new Vector2(0, 230);\n'
    elif 'titleRt.sizeDelta = new Vector2(1000, 416);' in line:
        lines[i] = '        titleRt.sizeDelta = new Vector2(750, 312);\n'
    
    # 2. Update button pos to center under new logo size
    elif '.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(310,' in line:
        lines[i] = lines[i].replace('new Vector2(310,', 'new Vector2(245,')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("HalloweenUIBuilder updated to shrink logo and center buttons under it")
