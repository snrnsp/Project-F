import sys
import re

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace yPos -= 80; (Preview Text)
content = re.sub(r'// Preview Text & Background \(to see opacity\)\s*yPos -= 80;', r'// Preview Text & Background (to see opacity)\n        yPos -= 100;', content)

# Replace yPos -= 75; (Auto-play Delay)
content = re.sub(r'// ─── 2. Auto-play Delay ───\s*yPos -= 75;', r'// ─── 2. Auto-play Delay ───\n        yPos -= 115;', content)

# Replace yPos -= 85; (Dialogue Box Opacity)
content = re.sub(r'// ─── 3. Dialogue Box Opacity ───\s*yPos -= 85;', r'// ─── 3. Dialogue Box Opacity ───\n        yPos -= 115;', content)

# Replace yPos -= 85; (Skip Mode)
content = re.sub(r'// ─── 4. Skip Mode \(toggle button\) ───\s*yPos -= 85;', r'// ─── 4. Skip Mode (toggle button) ───\n        yPos -= 115;', content)

# Replace yPos -= 55; (Font Style)
content = re.sub(r'// ─── 5. Font Style \(toggle button\) ───\s*yPos -= 55;', r'// ─── 5. Font Style (toggle button) ───\n        yPos -= 85;', content)


with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Regex replace applied")
