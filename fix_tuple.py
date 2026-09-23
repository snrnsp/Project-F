import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    file_text = f.read()

target = 'UIHelper.SetField(langUi, "closeText", closeTuple.txt);'
replacement = 'UIHelper.SetField(langUi, "closeText", closeTuple.text);'

if target in file_text:
    file_text = file_text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(file_text)
    print('Fixed tuple field name')
else:
    print('Target not found')
