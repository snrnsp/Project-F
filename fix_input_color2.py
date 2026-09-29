import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = 'Text autoPlayValueText = CreateLegacyText(inputTextObj, "2.0", new Color32(0, 0, 0, 255), 22, TextAnchor.MiddleCenter);'
new_code = 'Text autoPlayValueText = CreateLegacyText(inputTextObj, "2.0", new Color32(255, 255, 255, 255), 22, TextAnchor.MiddleCenter);'

content = content.replace(old_code, new_code)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Text color changed to white")
