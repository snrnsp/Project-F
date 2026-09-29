import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace('UnityEngine.UI.Outline outline = autoValObj.AddComponent<UnityEngine.UI.Outline>();', 'UnityEngine.UI.Outline inputOutline = autoValObj.AddComponent<UnityEngine.UI.Outline>();')
content = content.replace('outline.effectColor = HalloweenTheme.AccentOrange;\n        outline.effectDistance = new Vector2(2, -2);', 'inputOutline.effectColor = HalloweenTheme.AccentOrange;\n        inputOutline.effectDistance = new Vector2(2, -2);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print('Fixed outline variable scope issue')
