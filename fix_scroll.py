import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''            ScrollRect scrollRect = scrollObj\.AddComponent<ScrollRect>\(\);\r?\n\s*scrollRect\.horizontal = false;\r?\n\s*scrollRect\.vertical = true;'''
replacement = r'''            ScrollRect scrollRect = scrollObj.AddComponent<ScrollRect>();
            scrollRect.horizontal = false;
            scrollRect.vertical = true;
            scrollRect.scrollSensitivity = 45f;'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed scrollSensitivity for Backlog UI!")
else:
    print("Failed to match scrollSensitivity for Backlog UI!")
