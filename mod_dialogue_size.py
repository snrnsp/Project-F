import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('panelRt.offsetMin = new Vector2(50, 20); // padding', 'panelRt.offsetMin = new Vector2(180, 20); // padding reduced horizontal size')
text = text.replace('panelRt.offsetMax = new Vector2(-50, HalloweenTheme.DialoguePanelHeight + 20);', 'panelRt.offsetMax = new Vector2(-180, HalloweenTheme.DialoguePanelHeight + 20);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Reduced dialogue panel horizontal size')
