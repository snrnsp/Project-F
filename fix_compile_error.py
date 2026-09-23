import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = 'UIHelper.AddBorder(btnObj, HalloweenTheme.PanelBorder, HalloweenTheme.PanelBorderWidth);'
replacement = '''UnityEngine.UI.Outline outline = btnObj.AddComponent<UnityEngine.UI.Outline>();
            outline.effectColor = HalloweenTheme.PanelBorder;
            outline.effectDistance = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth);'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed AddBorder error in HalloweenUIBuilder')
