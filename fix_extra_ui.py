import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'GameObject titleObj = UIHelper.CreateUIObject("Title", headerObj.transform);' in line:
        # We found the CreateExtraUI title declaration.
        # It should be around line 1410
        # Let's replace the next few lines.
        lines[i+2] = '        UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));\n'
        lines[i+3] = '        titleRt.anchoredPosition = Vector2.zero;\n        titleRt.sizeDelta = new Vector2(400, 60);\n'
        break

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("HalloweenUIBuilder updated to fix ExtraUI title")
