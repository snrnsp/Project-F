import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = 'UIHelper.SetField(extraUi, "extraPanel", extraRoot);'
replacement = '''UIHelper.SetField(extraUi, "extraPanel", extraRoot);
            UIHelper.SetField(extraUi, "globalSettingsButton", globalSettingsBtnObj);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Fixed globalSettingsButton injection')
else:
    print('Target not found')
