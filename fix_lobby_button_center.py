import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # 1. Rollback logo anchor and pos
    if 'UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));' in line:
        lines[i] = '        UIHelper.SetAnchors(titleRt, new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));\n'
    elif 'titleRt.anchoredPosition = new Vector2(0, 230);' in line:
        lines[i] = '        titleRt.anchoredPosition = new Vector2(-60, 230);\n'
    
    # 2. Rollback button anchors and pos, but move pos to X=310 instead of 180 to center under logo
    elif 'UIHelper.SetAnchors(' in line and 'btn.GetComponent<RectTransform>' in line:
        lines[i] = lines[i].replace('new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0, 0.5f)', 'new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f)')
    elif '.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(-267,' in line:
        # 310 centers the 260px wide buttons under the 440px center of the logo text
        lines[i] = lines[i].replace('new Vector2(-267,', 'new Vector2(310,')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("HalloweenUIBuilder updated to rollback center and move buttons right")
