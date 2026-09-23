import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = 'lobbyTitleText.lineSpacing = 0.65f;'
replacement = '''lobbyTitleText.lineSpacing = 0.65f;
            UnityEngine.UI.Outline titleOutline = titleObj.AddComponent<UnityEngine.UI.Outline>();
            titleOutline.effectColor = new Color32(0, 0, 0, 255);
            titleOutline.effectDistance = new Vector2(2, -2);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('SUCCESS')
else:
    print('FAILED')
