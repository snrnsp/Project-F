import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace('inputTextRt.anchoredPosition = new Vector2(300, 3);', 'inputTextRt.anchoredPosition = new Vector2(310, 3);')

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Updated inputTextRt position to 310.")
