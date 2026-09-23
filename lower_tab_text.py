import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                // Shift text up slightly within the container so it's vertically balanced
                tabTextRt.offsetMin = new Vector2(0, 5);
                tabTextRt.offsetMax = new Vector2(0, 5);'''

replacement = '''                // Shift text down slightly to the dead center (removed previous +5 upward bias)
                tabTextRt.offsetMin = new Vector2(0, 0);
                tabTextRt.offsetMax = new Vector2(0, 0);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Adjusted tab text position downwards')
else:
    print('Target not found')
