import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('lobbyTitleText.fontStyle = FontStyle.Bold;', 'lobbyTitleText.fontStyle = FontStyle.Bold;\n            lobbyTitleText.lineSpacing = 0.65f;')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Adjusted line spacing for lobby title')
