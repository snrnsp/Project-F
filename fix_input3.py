import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Update inputTextRt size and position
content = content.replace('inputTextRt.anchoredPosition = new Vector2(310, 3);', 'inputTextRt.anchoredPosition = new Vector2(315, 3);')
content = content.replace('inputTextRt.sizeDelta = new Vector2(70, 30);', 'inputTextRt.sizeDelta = new Vector2(60, 30);')

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Updated inputTextRt size and position.")
