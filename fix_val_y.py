import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_val = '''        private Text CreateSettingsValueText(Transform parent, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject("VolumeValue", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(235, yPos);
            rt.sizeDelta = new Vector2(90, 30);
            Text t = CreateLegacyText(obj, "", HalloweenTheme.TextPrimary, 22, TextAnchor.MiddleCenter);
            t.raycastTarget = false;
            return t;
        }'''

new_val = '''        private Text CreateSettingsValueText(Transform parent, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject("VolumeValue", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(235, yPos + 3); // Visual alignment offset
            rt.sizeDelta = new Vector2(90, 30);
            Text t = CreateLegacyText(obj, "", HalloweenTheme.TextPrimary, 22, TextAnchor.MiddleCenter);
            t.raycastTarget = false;
            return t;
        }'''

if old_val in content:
    content = content.replace(old_val, new_val)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Updated CreateSettingsValueText yPos.")
else:
    print("Could not find CreateSettingsValueText.")
