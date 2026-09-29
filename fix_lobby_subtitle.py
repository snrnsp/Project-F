import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# 1. Update logo size and position
for i, line in enumerate(lines):
    if 'titleRt.anchoredPosition = new Vector2(250, 320);' in line:
        lines[i] = '        titleRt.anchoredPosition = new Vector2(300, 320);\n'
    elif 'titleRt.sizeDelta = new Vector2(500, 196);' in line:
        lines[i] = '        titleRt.sizeDelta = new Vector2(1500, 588); // scaled up by 3x\n'

# 2. Comment out subtitle creation
sub_start = -1
sub_end = -1
for i, line in enumerate(lines):
    if 'GameObject subTitleObj = UIHelper.CreateUIObject("LobbySubtitleText", lobbyPanelRoot.transform);' in line:
        sub_start = i
    if 'subOutline.effectDistance =' in line and sub_start != -1:
        sub_end = i
        break

if sub_start != -1 and sub_end != -1:
    for i in range(sub_start, sub_end + 1):
        lines[i] = '// ' + lines[i]

# Also comment out the SetField for subtitle so it doesn't cause errors
for i, line in enumerate(lines):
    if 'UIHelper.SetField(lobbyUi, "lobbySubtitleText", lobbySubtitleText);' in line:
        lines[i] = '// ' + lines[i]

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("HalloweenUIBuilder updated to enlarge logo and remove subtitle")
