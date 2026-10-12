import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'UIHelper.AddText(titleObj, Loc.Get("ui.builder.investigation.collected_evidence",' in line:
        # Go up and fix the two lines
        lines[i-2] = '            titleRt.anchoredPosition = new Vector2(0, -60);\n'
        lines[i-1] = '            titleRt.sizeDelta = new Vector2(400, 60);\n'
    if 'UIHelper.AddText(titleObj, Loc.Get("ui.builder.backlog.title",' in line:
        lines[i-2] = '            titleRt.anchoredPosition = new Vector2(0, -60);\n'
        lines[i-1] = '            titleRt.sizeDelta = new Vector2(400, 60);\n'

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Fixed mangled titles.")
