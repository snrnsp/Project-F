import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# 1. Update CreateSettingsLabel
content = re.sub(
    r'private Text CreateSettingsLabel\(Transform parent, string text, float yPos\)\s*{\s*GameObject obj = UIHelper.CreateUIObject\(text \+ "Label", parent\);\s*RectTransform rt = obj.GetComponent<RectTransform>\(\);\s*UIHelper.SetAnchors\(rt, new Vector2\(0.5f, 1\), new Vector2\(0.5f, 1\), new Vector2\(0.5f, 1\)\);\s*rt.anchoredPosition = new Vector2\(0, yPos\);\s*rt.sizeDelta = new Vector2\(400, 40\);\s*return CreateLegacyText\(obj, text, HalloweenTheme.TextPrimary, 24, TextAnchor.MiddleCenter\);\s*}',
    '''private Text CreateSettingsLabel(Transform parent, string text, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject(text + "Label", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(-170, yPos);
            rt.sizeDelta = new Vector2(280, 40);
            return CreateLegacyText(obj, text, HalloweenTheme.TextPrimary, 24, TextAnchor.MiddleRight);
        }''',
    content
)

# 2. Update CreateSettingsSlider
content = re.sub(
    r'private Slider CreateSettingsSlider\(Transform parent, float yPos\)\s*{\s*GameObject sliderObj = UIHelper.CreateUIObject\("Slider", parent\);\s*RectTransform rt = sliderObj.GetComponent<RectTransform>\(\);\s*UIHelper.SetAnchors\(rt, new Vector2\(0.5f, 1\), new Vector2\(0.5f, 1\), new Vector2\(0.5f, 1\)\);\s*rt.anchoredPosition = new Vector2\(0, yPos\);\s*rt.sizeDelta = new Vector2\(350, 20\);',
    '''private Slider CreateSettingsSlider(Transform parent, float yPos)
        {
            GameObject sliderObj = UIHelper.CreateUIObject("Slider", parent);
            RectTransform rt = sliderObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(100, yPos);
            rt.sizeDelta = new Vector2(240, 20);''',
    content
)

# 3. Update CreateSettingsValueText
content = re.sub(
    r'private Text CreateSettingsValueText\(Transform parent, float yPos\)\s*{\s*GameObject obj = UIHelper.CreateUIObject\("VolumeValue", parent\);\s*RectTransform rt = obj.GetComponent<RectTransform>\(\);\s*UIHelper.SetAnchors\(rt, new Vector2\(0.5f, 1\), new Vector2\(0.5f, 1\), new Vector2\(0.5f, 1\)\);\s*rt.anchoredPosition = new Vector2\(235, yPos\);\s*rt.sizeDelta = new Vector2\(90, 30\);\s*Text t = CreateLegacyText\(obj, "", HalloweenTheme.TextPrimary, 22, TextAnchor.MiddleCenter\);',
    '''private Text CreateSettingsValueText(Transform parent, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject("VolumeValue", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(260, yPos);
            rt.sizeDelta = new Vector2(70, 30);
            Text t = CreateLegacyText(obj, "", HalloweenTheme.TextPrimary, 20, TextAnchor.MiddleLeft);''',
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Regex replace components complete.")
