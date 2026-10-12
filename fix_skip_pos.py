import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix dropRt.anchoredPosition
content = re.sub(
    r'dropRt\.anchoredPosition = new Vector2\(100, yPos - 20 - 60\);',
    'dropRt.anchoredPosition = new Vector2(100, -480);',
    content
)

# Fix shpRt.anchoredPosition
content = re.sub(
    r'shpRt\.anchoredPosition = new Vector2\(0, yPos - 30\);',
    'shpRt.anchoredPosition = new Vector2(0, -450);',
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed Y positions for Skip Dropdown and Help Panel.")
