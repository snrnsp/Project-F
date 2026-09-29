import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace('UIHelper.AddImage(autoValObj, new Color32(0, 0, 0, 150));', 'UIHelper.AddImage(autoValObj, new Color32(0, 0, 0, 255));')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Background made opaque black")
