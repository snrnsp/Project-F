import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''cb\.fadeDuration = 0\.15f;'''
replacement = r'''cb.fadeDuration = 0.08f;'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed HalloweenUIBuilder fade durations!")
else:
    print("Failed to match HalloweenUIBuilder!")
