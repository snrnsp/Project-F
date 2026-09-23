import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('TextAnchor.MiddleLeft', 'TextAnchor.MiddleCenter')
text = text.replace('<size=30>', '<size=22>')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Centered title text and reduced subtitle size')
