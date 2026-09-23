import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            Image img = UIHelper.AddImage(btnObj, btnBg);
            Button btn = btnObj.AddComponent<Button>();'''

replacement = '''            Image img = UIHelper.AddImage(btnObj, btnBg);
            Button btn = btnObj.AddComponent<Button>();
            UIHelper.AddBorder(btnObj, HalloweenTheme.PanelBorder, HalloweenTheme.PanelBorderWidth);'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added borders to lobby buttons')
