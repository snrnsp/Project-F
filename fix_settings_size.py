import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Fix Settings Label
old_label = """        private Text CreateSettingsLabel(Transform parent, string text, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject(text + "Label", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(0, yPos);
            rt.sizeDelta = new Vector2(400, 25);
            return CreateLegacyText(obj, text, HalloweenTheme.TextPrimary, 18, TextAnchor.UpperLeft);
        }"""
new_label = """        private Text CreateSettingsLabel(Transform parent, string text, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject(text + "Label", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(0, yPos);
            rt.sizeDelta = new Vector2(400, 40);
            return CreateLegacyText(obj, text, HalloweenTheme.TextPrimary, 28, TextAnchor.UpperLeft);
        }"""

# Fix Title
old_title = """            titleRt.sizeDelta = new Vector2(400, 40);
            Text titleText = CreateLegacyText(titleObj, "설정", HalloweenTheme.AccentOrange, 32, TextAnchor.UpperCenter);"""
new_title = """            titleRt.sizeDelta = new Vector2(400, 55);
            Text titleText = CreateLegacyText(titleObj, "설정", HalloweenTheme.AccentOrange, 42, TextAnchor.UpperCenter);"""

# Fix Preview
old_preview = """            previewRt.sizeDelta = new Vector2(600, 40);
            Text previewText = CreateLegacyText(previewObj, "", HalloweenTheme.TextPrimary, 18, TextAnchor.MiddleCenter);"""
new_preview = """            previewRt.sizeDelta = new Vector2(600, 50);
            Text previewText = CreateLegacyText(previewObj, "", HalloweenTheme.TextPrimary, 32, TextAnchor.MiddleCenter);"""


if old_label in content: content = content.replace(old_label, new_label)
if old_title in content: content = content.replace(old_title, new_title)
if old_preview in content: content = content.replace(old_preview, new_preview)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("✅ Settings UI Text sizes updated")
