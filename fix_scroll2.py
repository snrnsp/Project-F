import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern2 = r'''                ScrollRect scrollRect = infoPanelObj\.AddComponent<ScrollRect>\(\);\r?\n\s*scrollRect\.horizontal = false;\r?\n\s*scrollRect\.vertical = true;\r?\n\s*scrollRect\.movementType = ScrollRect\.MovementType\.Clamped;'''
replacement2 = r'''                ScrollRect scrollRect = infoPanelObj.AddComponent<ScrollRect>();
                scrollRect.horizontal = false;
                scrollRect.vertical = true;
                scrollRect.movementType = ScrollRect.MovementType.Clamped;
                scrollRect.scrollSensitivity = 45f;'''

new_content = re.sub(pattern2, replacement2, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed scrollSensitivity for Extra UI!")
else:
    print("Failed to match scrollSensitivity for Extra UI!")
