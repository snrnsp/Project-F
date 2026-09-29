import sys
import re

path = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Pre-Alpha Title: 30 -> 45
content = content.replace(
    'Theme.UIHelper.AddText(iconObj, "Pre-Alpha 안내", new Color32(150, 200, 255, 255), 30,',
    'Theme.UIHelper.AddText(iconObj, "Pre-Alpha 안내", new Color32(150, 200, 255, 255), 45,'
)

# Pre-Alpha Body: 24 -> 36
content = content.replace(
    'Theme.UIHelper.AddText(msgObj, preAlphaMsg, new Color32(230, 230, 230, 255), 24,',
    'Theme.UIHelper.AddText(msgObj, preAlphaMsg, new Color32(230, 230, 230, 255), 36,'
)

# Seizure Title: 30 -> 45
content = content.replace(
    'Theme.UIHelper.AddText(iconObj, "광과민성 발작 경고", new Color32(255, 180, 80, 255), 30,',
    'Theme.UIHelper.AddText(iconObj, "광과민성 발작 경고", new Color32(255, 180, 80, 255), 45,'
)

# Seizure Body: 20 -> 32
content = content.replace(
    'new Color32(200, 195, 210, 255), 20, TextAlignmentOptions.Center);',
    'new Color32(200, 195, 210, 255), 32, TextAlignmentOptions.Center);'
)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("LobbyUI.cs updated to increase text size")
