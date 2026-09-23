import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            Image btnImg = btnObj.AddComponent<Image>();
            btnImg.color = new Color32(80, 50, 120, 255);
            Button btn = btnObj.AddComponent<Button>();
            ColorBlock cb = ColorBlock.defaultColorBlock;
            cb.normalColor = new Color32(80, 50, 120, 255);
            cb.highlightedColor = new Color32(110, 70, 160, 255);
            cb.pressedColor = new Color32(150, 100, 50, 255);
            btn.colors = cb;
            btn.targetGraphic = btnImg;

            GameObject btnTextObj = new GameObject("ButtonText");
            btnTextObj.transform.SetParent(btnObj.transform, false);
            RectTransform btnTextRt = btnTextObj.AddComponent<RectTransform>();
            btnTextRt.anchorMin = Vector2.zero;
            btnTextRt.anchorMax = Vector2.one;
            btnTextRt.offsetMin = Vector2.zero;
            btnTextRt.offsetMax = Vector2.zero;
            TextMeshProUGUI btnText = Theme.UIHelper.AddText(btnTextObj, "\ud655\uc778", new Color32(255, 255, 255, 255), 24, TextAlignmentOptions.Center);
            btnText.fontStyle = FontStyles.Bold;'''

replacement = '''            // Invisible hitbox
            Image hitImg = Theme.UIHelper.AddImage(btnObj, new Color(0, 0, 0, 0));

            // Border
            GameObject borderObj = new GameObject("Border");
            borderObj.transform.SetParent(btnObj.transform, false);
            RectTransform borderRt = borderObj.AddComponent<RectTransform>();
            borderRt.anchorMin = Vector2.zero;
            borderRt.anchorMax = Vector2.one;
            borderRt.offsetMin = Vector2.zero;
            borderRt.offsetMax = Vector2.zero;
            Image borderImg = Theme.UIHelper.AddImage(borderObj, new Color32(255, 150, 40, 255)); // Orange border
            borderImg.raycastTarget = false;

            // Background
            GameObject bgObj = new GameObject("Background");
            bgObj.transform.SetParent(btnObj.transform, false);
            RectTransform bgRt = bgObj.AddComponent<RectTransform>();
            bgRt.anchorMin = Vector2.zero;
            bgRt.anchorMax = Vector2.one;
            bgRt.offsetMin = new Vector2(4, 4);
            bgRt.offsetMax = new Vector2(-4, -4);
            Image bgImg = Theme.UIHelper.AddImage(bgObj, new Color32(80, 50, 120, 255));
            bgImg.raycastTarget = false;

            Button btn = btnObj.AddComponent<Button>();
            ColorBlock cb = ColorBlock.defaultColorBlock;
            cb.normalColor = Color.white;
            cb.highlightedColor = new Color32(200, 200, 200, 255);
            cb.pressedColor = new Color32(150, 150, 150, 255);
            btn.colors = cb;
            btn.targetGraphic = bgImg;

            GameObject btnTextObj = new GameObject("ButtonText");
            btnTextObj.transform.SetParent(btnObj.transform, false);
            RectTransform btnTextRt = btnTextObj.AddComponent<RectTransform>();
            btnTextRt.anchorMin = Vector2.zero;
            btnTextRt.anchorMax = Vector2.one;
            btnTextRt.offsetMin = Vector2.zero;
            btnTextRt.offsetMax = Vector2.zero;
            TextMeshProUGUI btnText = Theme.UIHelper.AddText(btnTextObj, "\ud655\uc778", new Color32(255, 255, 255, 255), 28, TextAlignmentOptions.Center);
            btnText.fontStyle = FontStyles.Bold;'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated OK button with border and larger text')
