import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace('dropRt.sizeDelta = new Vector2(240, 120);', 'dropRt.sizeDelta = new Vector2(350, 120);')

content = content.replace('var optCtrl = CreateLegacyButton(dropPanelObj.transform, "Ctrl", 240, 40, new Color32(50, 35, 70, 255));',
                          'var optCtrl = CreateLegacyButton(dropPanelObj.transform, "Ctrl", 350, 40, new Color32(50, 35, 70, 255));')
content = content.replace('var optShift = CreateLegacyButton(dropPanelObj.transform, "Shift", 240, 40, new Color32(50, 35, 70, 255));',
                          'var optShift = CreateLegacyButton(dropPanelObj.transform, "Shift", 350, 40, new Color32(50, 35, 70, 255));')
content = content.replace('var optSpace = CreateLegacyButton(dropPanelObj.transform, "Space", 240, 40, new Color32(50, 35, 70, 255));',
                          'var optSpace = CreateLegacyButton(dropPanelObj.transform, "Space", 350, 40, new Color32(50, 35, 70, 255));')

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Updated dropdown widths to 350.")
