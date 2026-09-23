import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('bgRt.offsetMin = new Vector2(4, 4);', 'bgRt.offsetMin = new Vector2(6, 6);')
text = text.replace('bgRt.offsetMax = new Vector2(-4, -4);', 'bgRt.offsetMax = new Vector2(-6, -6);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Increased border width to 6')
