import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '''            // Made the shadow box much smaller, shifted right/down for stack depth
            shadowRt.offsetMin = new Vector2(160, 70);
            shadowRt.offsetMax = new Vector2(-140, -160);'''

replacement1 = '''            // Shadow box encompassing the entire diagonal stack
            shadowRt.offsetMin = new Vector2(160, 20);
            shadowRt.offsetMax = new Vector2(-65, -135);'''

target2 = '''                // Staircase Y shift: Each subsequent folder is pushed UP by 30 pixels!
                float yShift = ci * 30f;
                folderRt.offsetMin = new Vector2(150, 80 + yShift);
                folderRt.offsetMax = new Vector2(-150, -150 + yShift);'''

replacement2 = '''                // Diagonal staircase: Shift UP by 15px and RIGHT by 15px (tighter overlap)
                // Base Y is moved down by 50px to make room for the stack at the top
                float xShift = ci * 15f;
                float yShift = ci * 15f;
                folderRt.offsetMin = new Vector2(150 + xShift, 30 + yShift);
                folderRt.offsetMax = new Vector2(-150 + xShift, -200 + yShift);'''

if target1 in text and target2 in text:
    text = text.replace(target1, replacement1).replace(target2, replacement2)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated folders to be diagonal, tighter, and lower')
else:
    print('Targets not found')
