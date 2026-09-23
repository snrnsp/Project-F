import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Change titleY
target1 = 'float titleY = -52f;'
replacement1 = 'float titleY = -75f;'

# Change OK button Y
target2 = 'btnRt.anchoredPosition = new Vector2(0, 45);'
replacement2 = 'btnRt.anchoredPosition = new Vector2(0, 70);'

if target1 in text and target2 in text:
    text = text.replace(target1, replacement1)
    text = text.replace(target2, replacement2)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Adjusted positions of warning title and confirm button')
else:
    print('Could not find target strings')
