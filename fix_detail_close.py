import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = 'var closeTuple = UIHelper.CreateButton(detailPanel.transform, "닫기", 200, 50);'
replacement = 'var closeTuple = CreateLegacyButton(detailPanel.transform, "닫기", 200, 50, HalloweenTheme.ButtonNormal);'

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated DetailPanel close button properly')
