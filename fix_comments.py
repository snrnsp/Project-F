import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'/// <summary>\r?\n\s*/// Screen X \(anchor center\).*?</summary>'

replacement = r'''/// <summary>
        /// Screen X (anchor center) per slot. Fixed positions: Left=25%, Center=50%, Right=75%.
        /// Prevents characters from sliding around when other characters enter/exit.
        /// </summary>'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed comments!")
else:
    print("Failed to match comments!")
