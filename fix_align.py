import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('legacyText.alignment = TextAnchor.MiddleCenter;', 'legacyText.alignment = TextAnchor.MiddleCenter;\n            legacyText.alignByGeometry = true;')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added alignByGeometry to Legacy Text')
