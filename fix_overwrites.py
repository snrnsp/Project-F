import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace label overwrites
content = re.sub(r'\.anchoredPosition = new Vector2\(-300, 0\);', '.anchoredPosition = new Vector2(-300, 4);', content)

# Replace value text overwrites (300, 0) -> (300, 3)
content = re.sub(r'ValueText\.GetComponent<RectTransform>\(\)\.anchoredPosition = new Vector2\(300, 0\);', 
                 'ValueText.GetComponent<RectTransform>().anchoredPosition = new Vector2(300, 3);', content)

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Updated anchoredPosition overwrites to preserve Y offsets.")
