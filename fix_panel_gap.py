import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            unifiedBgRt.offsetMin = new Vector2(40, 20);
            unifiedBgRt.offsetMax = new Vector2(-20, -150);'''

replacement = '''            unifiedBgRt.offsetMin = new Vector2(40, 20);
            unifiedBgRt.offsetMax = new Vector2(-20, -115); // Closed the gap between tabs and panel'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Closed vertical gap between tabs and panel')
else:
    print('Target not found')
