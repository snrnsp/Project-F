import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('legacyText.fontSize = fontSize;', 'legacyText.fontSize = fontSize;\n            legacyText.alignByGeometry = true;')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added alignByGeometry globally for Legacy Text')
