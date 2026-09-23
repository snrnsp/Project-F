import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''                if (isSelected)
                {
                    // Bring selected folder to front
                    folder.transform.SetAsLastSibling();
                    
                    // Move to center/active position
                    rt.offsetMin = new Vector2(150, 30);
                    rt.offsetMax = new Vector2(-150, -200);'''

replacement = '''                if (isSelected)
                {
                    // Bring selected folder to front
                    folder.transform.SetAsLastSibling();
                    
                    // Move to center/active position
                    rt.offsetMin = new Vector2(150, 10);
                    rt.offsetMax = new Vector2(-150, -220);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated ExtraUI active position to match new lower base')
else:
    print('Target not found')
