import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<size=30>', '<size=22>')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated subtitle size in LobbyUI.cs')
