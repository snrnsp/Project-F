import sys
import re

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Make the panel slightly taller just in case
content = content.replace('panelRt.sizeDelta = new Vector2(700, 750);', 'panelRt.sizeDelta = new Vector2(700, 800);')

# Update spacings to be slightly tighter
content = re.sub(r'float yPos = -100;', r'float yPos = -85;', content)

content = re.sub(r'// Preview Text & Background \(to see opacity\)\s*yPos -= 100;', r'// Preview Text & Background (to see opacity)\n        yPos -= 90;', content)

content = re.sub(r'// ─── 2\. Auto-play Delay ───\s*yPos -= 115;', r'// ─── 2. Auto-play Delay ───\n        yPos -= 95;', content)

content = re.sub(r'// ─── 3\. Dialogue Box Opacity ───\s*yPos -= 115;', r'// ─── 3. Dialogue Box Opacity ───\n        yPos -= 100;', content)

content = re.sub(r'// ─── 4\. Skip Mode \(toggle button\) ───\s*yPos -= 115;', r'// ─── 4. Skip Mode (toggle button) ───\n        yPos -= 100;', content)

content = re.sub(r'// ─── 5\. Font Style \(toggle button\) ───\s*yPos -= 85;', r'// ─── 5. Font Style (toggle button) ───\n        yPos -= 80;', content)


with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Settings UI layout adjusted again")
