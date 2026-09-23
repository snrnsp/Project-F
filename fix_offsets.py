import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target1 = '''        private int currentIndex = 0;

        // Folder colors (real manila folder look)'''

replacement1 = '''        private int currentIndex = 0;
        
        public List<Vector2> defaultOffsetMins = new List<Vector2>();
        public List<Vector2> defaultOffsetMaxs = new List<Vector2>();

        // Folder colors (real manila folder look)'''

if target1 in text:
    text = text.replace(target1, replacement1)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Successfully added defaultOffsetMins')
else:
    print('Target not found')
