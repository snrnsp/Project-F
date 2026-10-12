import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CreateSettingsLabel
old_label = '''        private Text CreateSettingsLabel(Transform parent, string label, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject("Label_" + label, parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(0, yPos);
            rt.sizeDelta = new Vector2(400, 40);
            return CreateLegacyText(obj, label, HalloweenTheme.TextPrimary, 24, TextAnchor.MiddleCenter);
        }'''
new_label = '''        private Text CreateSettingsLabel(Transform parent, string label, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject("Label_" + label, parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(-170, yPos);
            rt.sizeDelta = new Vector2(280, 40);
            return CreateLegacyText(obj, label, HalloweenTheme.TextPrimary, 24, TextAnchor.MiddleRight);
        }'''

# 2. Update CreateSettingsSlider
old_slider = '''        private Slider CreateSettingsSlider(Transform parent, float yPos)
        {
            GameObject sliderObj = UIHelper.CreateUIObject("Slider", parent);
            RectTransform rt = sliderObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(0, yPos);
            rt.sizeDelta = new Vector2(400, 20);'''
new_slider = '''        private Slider CreateSettingsSlider(Transform parent, float yPos)
        {
            GameObject sliderObj = UIHelper.CreateUIObject("Slider", parent);
            RectTransform rt = sliderObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(100, yPos);
            rt.sizeDelta = new Vector2(240, 20);'''

# 3. Update CreateSettingsValueText
old_value = '''        private Text CreateSettingsValueText(Transform parent, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject("VolumeValue", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(235, yPos);
            rt.sizeDelta = new Vector2(90, 30);
            Text t = CreateLegacyText(obj, "", HalloweenTheme.TextPrimary, 22, TextAnchor.MiddleCenter);'''
new_value = '''        private Text CreateSettingsValueText(Transform parent, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject("VolumeValue", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(260, yPos);
            rt.sizeDelta = new Vector2(70, 30);
            Text t = CreateLegacyText(obj, "", HalloweenTheme.TextPrimary, 20, TextAnchor.MiddleLeft);'''

content = content.replace(old_label, new_label)
content = content.replace(old_slider, new_slider)
content = content.replace(old_value, new_value)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated basic settings layout components.")
