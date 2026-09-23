import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '''            shadowRt.offsetMin = new Vector2(35, 15);
            shadowRt.offsetMax = new Vector2(-15, -80);'''

replacement1 = '''            // Made the shadow box much smaller, shifted right/down for stack depth
            shadowRt.offsetMin = new Vector2(160, 70);
            shadowRt.offsetMax = new Vector2(-140, -160);'''

target2 = '''                folderRt.offsetMin = new Vector2(40, 20);
                folderRt.offsetMax = new Vector2(-20, -85);'''

replacement2 = '''                // Made the overall folder noticeably smaller
                folderRt.offsetMin = new Vector2(150, 80);
                folderRt.offsetMax = new Vector2(-150, -150);'''

if target1 in text and target2 in text:
    text = text.replace(target1, replacement1).replace(target2, replacement2)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated folder and shadow box sizes')
else:
    print('Targets not found')
