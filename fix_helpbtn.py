import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace('skipHelpRt.anchoredPosition = new Vector2(-15, 0);', 'skipHelpRt.anchoredPosition = new Vector2(-50, 0);')

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Updated HelpButton position.")
