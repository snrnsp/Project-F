import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_bg = '''            // Background
            GameObject bgObj = UIHelper.CreateUIObject("Background", lobbyPanelRoot.transform);
            UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
            Sprite bgSprite = null;'''

new_bg = '''            // Background
            GameObject bgObj = UIHelper.CreateUIObject("Background", lobbyPanelRoot.transform);
            UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
            bgObj.GetComponent<RectTransform>().offsetMin = new Vector2(-2, -2);
            bgObj.GetComponent<RectTransform>().offsetMax = new Vector2(2, 2);
            Sprite bgSprite = null;'''

if old_bg in content:
    content = content.replace(old_bg, new_bg)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Added bleed to lobby bg.")
else:
    print("Could not find Lobby BG.")
