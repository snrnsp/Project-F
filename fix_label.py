import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CreateSettingsLabel
content = re.sub(
    r'private Text CreateSettingsLabel\(Transform parent, string text, float yPos\)\s*{\s*GameObject obj = UIHelper\.CreateUIObject\(text \+ "Label", parent\);\s*RectTransform rt = obj\.GetComponent<RectTransform>\(\);\s*UIHelper\.SetAnchors\(rt, new Vector2\(0\.5f, 1\), new Vector2\(0\.5f, 1\), new Vector2\(0\.5f, 1\)\);\s*rt\.anchoredPosition = new Vector2\(0, yPos\);\s*rt\.sizeDelta = new Vector2\(400, 40\);\s*return CreateLegacyText\(obj, text, HalloweenTheme\.TextPrimary, 28, TextAnchor\.MiddleCenter\);\s*}',
    '''private Text CreateSettingsLabel(Transform parent, string text, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject(text + "Label", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(-160, yPos);
            rt.sizeDelta = new Vector2(280, 40);
            return CreateLegacyText(obj, text, HalloweenTheme.TextPrimary, 26, TextAnchor.MiddleRight);
        }''',
    content
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("CreateSettingsLabel fixed.")
