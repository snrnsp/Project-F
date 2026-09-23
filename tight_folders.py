import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '''            // Shadow box encompassing the entire diagonal stack
            shadowRt.offsetMin = new Vector2(160, 20);
            shadowRt.offsetMax = new Vector2(-65, -135);'''

replacement1 = '''            // Shadow box encompassing the entire diagonal stack (lowered and tightened)
            shadowRt.offsetMin = new Vector2(160, 0);
            shadowRt.offsetMax = new Vector2(-100, -170);'''

target2 = '''                // Diagonal staircase: Shift UP by 15px and RIGHT by 15px (tighter overlap)
                // Base Y is moved down by 50px to make room for the stack at the top
                float xShift = ci * 15f;
                float yShift = ci * 15f;
                folderRt.offsetMin = new Vector2(150 + xShift, 30 + yShift);
                folderRt.offsetMax = new Vector2(-150 + xShift, -200 + yShift);'''

replacement2 = '''                // Diagonal staircase: Shift UP by 8px and RIGHT by 8px (very tight overlap)
                // Base Y is lowered further to 10 and -220
                float xShift = ci * 8f;
                float yShift = ci * 8f;
                folderRt.offsetMin = new Vector2(150 + xShift, 10 + yShift);
                folderRt.offsetMax = new Vector2(-150 + xShift, -220 + yShift);'''

target3 = '''                float tabFraction = 1f / folderCount;
                float tabLeft = tabFraction * ci;
                float tabRight = tabFraction * (ci + 1);'''

replacement3 = '''                float tabFraction = 1f / folderCount;
                float tabLeft = tabFraction * ci;
                // Add extra width to tabs so they physically overlap each other!
                float tabRight = UnityEngine.Mathf.Min(1f, tabFraction * (ci + 1) + 0.03f);'''

if target1 in text and target2 in text and target3 in text:
    text = text.replace(target1, replacement1).replace(target2, replacement2).replace(target3, replacement3)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated HalloweenUIBuilder for lower, tighter stack with overlapping tabs')
else:
    print('Targets not found')
