import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace CreateSettingsLabel yPos
old_label = '''        private Text CreateSettingsLabel(Transform parent, string text, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject(text + "Label", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(0, yPos);
            rt.sizeDelta = new Vector2(400, 40);
            return CreateLegacyText(obj, text, HalloweenTheme.TextPrimary, 28, TextAnchor.MiddleRight);
        }'''

new_label = '''        private Text CreateSettingsLabel(Transform parent, string text, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject(text + "Label", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(0, yPos + 4); // Moved up 4 pixels to visually align with sliders
            rt.sizeDelta = new Vector2(400, 40);
            return CreateLegacyText(obj, text, HalloweenTheme.TextPrimary, 28, TextAnchor.MiddleRight);
        }'''

if old_label in content:
    content = content.replace(old_label, new_label)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Updated CreateSettingsLabel yPos.")
else:
    print("Could not find CreateSettingsLabel.")
