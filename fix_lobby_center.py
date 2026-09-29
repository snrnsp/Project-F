import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # Logo anchor and pos
    if 'UIHelper.SetAnchors(titleRt, new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));' in line:
        lines[i] = '        UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));\n'
    elif 'titleRt.anchoredPosition = new Vector2(-60, 230);' in line:
        lines[i] = '        titleRt.anchoredPosition = new Vector2(0, 230);\n'
    
    # Button anchors and pos
    elif 'UIHelper.SetAnchors(' in line and 'btn.GetComponent<RectTransform>' in line:
        lines[i] = lines[i].replace('new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f)', 'new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0, 0.5f)')
    elif '.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180,' in line:
        lines[i] = lines[i].replace('new Vector2(180,', 'new Vector2(-267,')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("HalloweenUIBuilder updated to center the Lobby UI")
