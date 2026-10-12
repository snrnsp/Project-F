import codecs

filepath = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace("overlay.transform.SetParent(lobbyPanel.transform.parent, false);", "overlay.transform.SetParent(lobbyPanel.transform, false);")

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
