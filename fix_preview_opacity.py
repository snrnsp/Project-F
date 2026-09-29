import sys

# 1. Update SettingsUI.cs
path = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Add field
old_field = "        [SerializeField] private Text opacityLabel;"
new_field = "        [SerializeField] private Text opacityLabel;\n        [SerializeField] private Image previewBoxImage;"
content = content.replace(old_field, new_field)

# Update OnOpacityChanged
old_op = """        private void OnOpacityChanged(float val)
        {
            SettingsData.DialogueBoxOpacity = val;
            // Apply opacity to DialogueUI in real-time
            var dialogueUI = Object.FindAnyObjectByType<DialogueUI>(FindObjectsInactive.Include);
            if (dialogueUI != null) dialogueUI.ApplyOpacity(val);
        }"""
new_op = """        private void OnOpacityChanged(float val)
        {
            SettingsData.DialogueBoxOpacity = val;
            
            if (previewBoxImage != null)
            {
                Color c = previewBoxImage.color;
                c.a = val;
                previewBoxImage.color = c;
            }

            // Apply opacity to DialogueUI in real-time
            var dialogueUI = Object.FindAnyObjectByType<DialogueUI>(FindObjectsInactive.Include);
            if (dialogueUI != null) dialogueUI.ApplyOpacity(val);
        }"""
content = content.replace(old_op, new_op)

# Set initial opacity in Show()
old_show = "                if (opacitySlider != null) opacitySlider.value = SettingsData.DialogueBoxOpacity;"
new_show = """                if (opacitySlider != null) opacitySlider.value = SettingsData.DialogueBoxOpacity;
                if (previewBoxImage != null)
                {
                    Color c = previewBoxImage.color;
                    c.a = SettingsData.DialogueBoxOpacity;
                    previewBoxImage.color = c;
                }"""
content = content.replace(old_show, new_show)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("1 SettingsUI.cs updated")

# 2. Update HalloweenUIBuilder.cs
path2 = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path2, 'r', encoding='utf-8-sig') as f:
    content2 = f.read()

old_preview = """            // Preview Text
            yPos -= 65;
            GameObject previewObj = UIHelper.CreateUIObject("PreviewText", panel.transform);
            RectTransform previewRt = previewObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(previewRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            previewRt.anchoredPosition = new Vector2(0, yPos);
            previewRt.sizeDelta = new Vector2(600, 40);
            Text previewText = CreateLegacyText(previewObj, "", HalloweenTheme.TextPrimary, 24, TextAnchor.MiddleCenter);"""

new_preview = """            // Preview Text & Background (to see opacity)
            yPos -= 65;
            
            // Bright background for contrast
            GameObject previewBgObj = UIHelper.CreateUIObject("PreviewGameBg", panel.transform);
            RectTransform pbgRt = previewBgObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(pbgRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            pbgRt.anchoredPosition = new Vector2(0, yPos);
            pbgRt.sizeDelta = new Vector2(620, 60);
            // Orange/brownish color to contrast with dark purple
            UIHelper.AddImage(previewBgObj, new Color32(200, 150, 100, 255));
            
            // The Box itself (simulates Dialogue panel)
            GameObject previewBoxObj = UIHelper.CreateUIObject("PreviewBox", previewBgObj.transform);
            RectTransform pboxRt = previewBoxObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(pboxRt);
            Color boxColor = HalloweenTheme.PanelBackground;
            boxColor.a = SettingsData.DialogueBoxOpacity;
            Image previewBoxImg = UIHelper.AddImage(previewBoxObj, boxColor);

            // The Text
            GameObject previewTextObj = UIHelper.CreateUIObject("PreviewText", previewBoxObj.transform);
            RectTransform ptextRt = previewTextObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(ptextRt);
            Text previewText = CreateLegacyText(previewTextObj, "", HalloweenTheme.TextPrimary, 24, TextAnchor.MiddleCenter);"""
content2 = content2.replace(old_preview, new_preview)

# Inject SetField for previewBoxImage
old_setfield = 'UIHelper.SetField(settingsUi, "previewTextLabel", previewText);'
new_setfield = 'UIHelper.SetField(settingsUi, "previewTextLabel", previewText);\n            UIHelper.SetField(settingsUi, "previewBoxImage", previewBoxImg);'
content2 = content2.replace(old_setfield, new_setfield)

with open(path2, 'w', encoding='utf-8-sig') as f:
    f.write(content2)
print("2 HalloweenUIBuilder.cs updated")
