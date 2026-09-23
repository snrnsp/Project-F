import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            delCb.pressedColor = new Color32(120, 10, 10, 255);      // Deep red when pressed
            deleteTuple.btn.colors = delCb;'''

replacement = '''            delCb.pressedColor = new Color32(120, 10, 10, 255);      // Deep red when pressed
            deleteTuple.btn.colors = delCb;
            
            // Remove hover script to ensure absolutely zero hover reaction
            Component hoverScript = deleteTuple.btn.GetComponent("LobbyButtonHover");
            if (hoverScript != null) UnityEngine.Object.Destroy(hoverScript);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Removed hover script from delete button')
else:
    print('Target not found')
