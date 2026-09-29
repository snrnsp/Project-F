import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Make the changes
content = content.replace('float yPos = -75;', 'float yPos = -100;')

# Replace preview yPos
content = content.replace("""// Preview Text & Background (to see opacity)
        yPos -= 80;""", """// Preview Text & Background (to see opacity)
        yPos -= 90;""")

# Replace autoPlay yPos
content = content.replace("""// ─── 2. Auto-play Delay ───
        yPos -= 75;""", """// ─── 2. Auto-play Delay ───
        yPos -= 110;""")

# Replace opacity yPos
content = content.replace("""// ─── 3. Dialogue Box Opacity ───
        yPos -= 85;""", """// ─── 3. Dialogue Box Opacity ───
        yPos -= 110;""")

# Replace skipMode yPos
content = content.replace("""// ─── 4. Skip Mode (toggle button) ───
        yPos -= 85;""", """// ─── 4. Skip Mode (toggle button) ───
        yPos -= 110;""")

# Replace fontStyle yPos
content = content.replace("""// ─── 5. Font Style (toggle button) ───
        yPos -= 55;""", """// ─── 5. Font Style (toggle button) ───
        yPos -= 85;""")

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Settings UI layout spaced out successfully")
