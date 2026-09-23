import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/UIHelper.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Revert auto-sizing in AddText
text = text.replace('tmp.alignment = alignment;\n            tmp.enableAutoSizing = true;\n            tmp.fontSizeMin = 10f;\n            tmp.fontSizeMax = fontSize;', 'tmp.alignment = alignment;')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Reverted global auto-sizing')
