import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace('autoPlayValueText.GetComponent<RectTransform>().sizeDelta = new Vector2(70, 30);', 'autoPlayValueText.GetComponent<RectTransform>().sizeDelta = new Vector2(0, 0);')

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Fixed autoPlayValueText sizeDelta.")
