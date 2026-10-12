import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/LobbyButtonHover.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''        private const float FADE_DURATION = 0\.15f;'''
replacement = r'''        private const float FADE_DURATION = 0.08f;'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed LobbyButtonHover!")
else:
    print("Failed to match LobbyButtonHover!")
