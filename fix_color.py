import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('HalloweenTheme.TextSecondary', 'new Color32(200, 190, 210, 255)')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed TextSecondary error.")
