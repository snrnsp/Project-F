import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# We need to replace the entire CreateLegacyButton body
target = '''        private (Button btn, Text text) CreateLegacyButton(Transform parent, string label, float width, float height, Color32 btnBg)
        {
            GameObject btnObj = UIHelper.CreateUIObject("Button_" + label, parent);
            RectTransform rt = btnObj.GetComponent<RectTransform>();
            rt.sizeDelta = new Vector2(width, height);

            Image img = UIHelper.AddImage(btnObj, btnBg);
            Button btn = btnObj.AddComponent<Button>();
            GameObject borderObj = UIHelper.CreateUIObject("Border", btnObj.transform);
            UIHelper.StretchFull(borderObj.GetComponent<RectTransform>());
            Image borderImg = borderObj.AddComponent<Image>();
            borderImg.color = new Color(1, 1, 1, 0);
            borderImg.raycastTarget = false;
            UnityEngine.UI.Outline outline = borderObj.AddComponent<UnityEngine.UI.Outline>();
            outline.effectColor = HalloweenTheme.PanelBorder;
            outline.effectDistance = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth);
            outline.useGraphicAlpha = false;
            btn.transition = Selectable.Transition.ColorTint;
            btn.colors = HalloweenTheme.GetButtonColors();
            btn.targetGraphic = img;

            GameObject textObj = UIHelper.CreateUIObject("Text", btnObj.transform);'''

replacement = '''        private (Button btn, Text text) CreateLegacyButton(Transform parent, string label, float width, float height, Color32 btnBg)
        {
            GameObject btnObj = UIHelper.CreateUIObject("Button_" + label, parent);
            RectTransform rt = btnObj.GetComponent<RectTransform>();
            rt.sizeDelta = new Vector2(width, height);

            // Invisible hit box
            Image hitImg = UIHelper.AddImage(btnObj, new Color(0, 0, 0, 0));

            // Border (drawn behind)
            GameObject borderObj = UIHelper.CreateUIObject("Border", btnObj.transform);
            UIHelper.StretchFull(borderObj.GetComponent<RectTransform>());
            Image borderImg = UIHelper.AddImage(borderObj, HalloweenTheme.PanelBorder);
            borderImg.raycastTarget = false;

            // Background (drawn on top, shrunk to reveal border)
            GameObject bgObj = UIHelper.CreateUIObject("Background", btnObj.transform);
            RectTransform bgRt = bgObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(bgRt);
            bgRt.offsetMin = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth);
            bgRt.offsetMax = new Vector2(-HalloweenTheme.PanelBorderWidth, -HalloweenTheme.PanelBorderWidth);
            Image bgImg = UIHelper.AddImage(bgObj, btnBg);
            bgImg.raycastTarget = false;

            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            btn.colors = HalloweenTheme.GetButtonColors();
            btn.targetGraphic = bgImg; // Only tint the inner background!

            GameObject textObj = UIHelper.CreateUIObject("Text", btnObj.transform);'''

if target in text:
    text = text.replace(target, replacement)
else:
    print('Target not found. Doing regex replacement.')
    import re
    pattern = r'private \(Button btn, Text text\) CreateLegacyButton\(Transform parent, string label, float width, float height, Color32 btnBg\)\s*\{.*?GameObject textObj = UIHelper\.CreateUIObject\("Text", btnObj\.transform\);'
    text = re.sub(pattern, replacement.strip(), text, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Redesigned button border logic')
