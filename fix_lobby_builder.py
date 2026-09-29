import sys
import re

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace Title Text creation
old_title_code = """        // Title Text (Top Left)
        GameObject titleObj = UIHelper.CreateUIObject("LobbyTitleText", lobbyPanelRoot.transform);
        RectTransform titleRt = titleObj.GetComponent<RectTransform>();
        UIHelper.SetAnchors(titleRt, new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
        titleRt.anchoredPosition = new Vector2(110, 320);
        titleRt.sizeDelta = new Vector2(400, 60);
        Text lobbyTitleText = CreateLegacyText(titleObj, "오블리비언", new Color32(255, 150, 40, 255), 56, TextAnchor.MiddleCenter);
        lobbyTitleText.fontStyle = FontStyle.Bold;"""

new_title_code = """        // Title Logo Image (Top Left)
        GameObject titleObj = UIHelper.CreateUIObject("LobbyTitleLogo", lobbyPanelRoot.transform);
        RectTransform titleRt = titleObj.GetComponent<RectTransform>();
        UIHelper.SetAnchors(titleRt, new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
        titleRt.anchoredPosition = new Vector2(110, 320);
        titleRt.sizeDelta = new Vector2(500, 196); // 1999x786 aspect ratio
        Image lobbyTitleLogo = UIHelper.AddImage(titleObj, Color.white);
        lobbyTitleLogo.preserveAspect = true;"""

content = content.replace(old_title_code, new_title_code)

# Replace SetField in HalloweenUIBuilder
content = content.replace('UIHelper.SetField(lobbyUi, "lobbyTitleText", lobbyTitleText);', 'UIHelper.SetField(lobbyUi, "logoImage", lobbyTitleLogo);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("HalloweenUIBuilder updated for Logo")
