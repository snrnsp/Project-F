import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Lobby Background Bleed
lobby_bg = '''              GameObject bgObj = UIHelper.CreateUIObject("Background", lobbyPanelRoot.transform);
              UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());'''

lobby_bg_new = '''              GameObject bgObj = UIHelper.CreateUIObject("Background", lobbyPanelRoot.transform);
              UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
              bgObj.GetComponent<RectTransform>().offsetMin = new Vector2(-5, -5);
              bgObj.GetComponent<RectTransform>().offsetMax = new Vector2(5, 5);'''

if lobby_bg in content:
    content = content.replace(lobby_bg, lobby_bg_new)
    print("Added bleed to Lobby Background.")
else:
    print("Could not find Lobby Background.")

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
