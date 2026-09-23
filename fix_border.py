import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            UnityEngine.UI.Outline outline = btnObj.AddComponent<UnityEngine.UI.Outline>();
            outline.effectColor = HalloweenTheme.PanelBorder;
            outline.effectDistance = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth);'''

replacement = '''            GameObject borderObj = UIHelper.CreateUIObject("Border", btnObj.transform);
            UIHelper.StretchFull(borderObj.GetComponent<RectTransform>());
            Image borderImg = borderObj.AddComponent<Image>();
            borderImg.color = new Color(1, 1, 1, 0);
            borderImg.raycastTarget = false;
            UnityEngine.UI.Outline outline = borderObj.AddComponent<UnityEngine.UI.Outline>();
            outline.effectColor = HalloweenTheme.PanelBorder;
            outline.effectDistance = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth);
            outline.useGraphicAlpha = false;'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated border implementation')
