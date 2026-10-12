import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'btnRt\.anchoredPosition = new Vector2\(-20, -20\);'
replacement = r'btnRt.anchoredPosition = new Vector2(-80, -40); // Moved inward for Verse8 safe area'

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Moved GlobalSettingsBtn inward!")
else:
    print("Failed to match GlobalSettingsBtn position!")
