import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('legacyText.alignByGeometry = true;', 'legacyText.alignByGeometry = true;\n            legacyText.verticalOverflow = VerticalWrapMode.Overflow;')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Enabled vertical overflow for Legacy Text')
