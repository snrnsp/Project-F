import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'scaler\.matchWidthOrHeight = 0\.5f;'

replacement = r'''scaler.matchWidthOrHeight = 1f; // Force Match Height to prevent vertical cutoff in web iframes'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed CanvasScaler matchWidthOrHeight!")
else:
    print("Failed to match CanvasScaler!")
