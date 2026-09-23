import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Change Title anchors and position
target_title = '''            UIHelper.SetAnchors(titleRt, new Vector2(0, 1), new Vector2(0, 1), new Vector2(0, 1));
            titleRt.anchoredPosition = new Vector2(80, -60);'''
replacement_title = '''            UIHelper.SetAnchors(titleRt, new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            titleRt.anchoredPosition = new Vector2(110, 310);'''
text = text.replace(target_title, replacement_title)

# Change Buttons X from 100 to 180
text = text.replace('new Vector2(100, startY', 'new Vector2(180, startY')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Moved UI to the right and positioned title above buttons')
