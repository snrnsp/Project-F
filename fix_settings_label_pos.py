import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace all Label anchoredPositions from -280 to -300
content = re.sub(r'(Label\.GetComponent<RectTransform>\(\)\.anchoredPosition = new Vector2\()(-280)(, 0\);)', r'\g<1>-300\g<3>', content)

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Updated Label anchored positions to -300.")
