import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Skip Mode
old_skip = '''            // 〓〓〓 3. Skip Mode (Dropdown) 〓〓〓
            yPos -= 85;
            var skipModeLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.builder.settings.skip_key", "스킵 단축키"), yPos);
            skipModeLabel.horizontalOverflow = HorizontalWrapMode.Overflow;
            // Add ContentSizeFitter to fit the text exactly so we can anchor the help button to its right
            UnityEngine.UI.ContentSizeFitter labelFitter = skipModeLabel.gameObject.AddComponent<UnityEngine.UI.ContentSizeFitter>();
            labelFitter.horizontalFit = UnityEngine.UI.ContentSizeFitter.FitMode.PreferredSize;

            // Help Button (?)
            GameObject skipHelpBtnObj = UIHelper.CreateUIObject("HelpButton", skipModeLabel.transform);
            RectTransform skipHelpRt = skipHelpBtnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(skipHelpRt, new Vector2(1, 0.5f), new Vector2(1, 0.5f), new Vector2(0, 0.5f));
            skipHelpRt.anchoredPosition = new Vector2(-5, 0); // -5px offset to account for internal padding
            skipHelpRt.sizeDelta = new Vector2(30, 30);
            UIHelper.AddImage(skipHelpBtnObj, new Color(0, 0, 0, 0)); // Invisible hit box
            Button skipHelpBtn = skipHelpBtnObj.AddComponent<Button>();
            skipHelpBtnObj.AddComponent<UIHoverSound>();
            GameObject skipHelpBtnTextObj = UIHelper.CreateUIObject("Text", skipHelpBtnObj.transform);
            RectTransform shtRt = skipHelpBtnTextObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(shtRt);
            Text skipHelpText = CreateLegacyText(skipHelpBtnTextObj, "?", HalloweenTheme.AccentOrange, 22, TextAnchor.MiddleCenter);
            skipHelpText.fontStyle = FontStyle.Bold;

            // The main dropdown button
            var skipTuple = CreateLegacyButton(panel.transform, "Ctrl ▼", 220, 40, new Color32(60, 40, 80, 255));
            RectTransform skipRt = skipTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(skipRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            skipRt.anchoredPosition = new Vector2(0, yPos - 45);'''

new_skip = '''            // 〓〓〓 3. Skip Mode (Dropdown) 〓〓〓
            yPos -= 65;
            var skipModeLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.builder.settings.skip_key", "스킵 단축키"), yPos);
            skipModeLabel.horizontalOverflow = HorizontalWrapMode.Overflow;
            // Add ContentSizeFitter to fit the text exactly so we can anchor the help button to its right
            UnityEngine.UI.ContentSizeFitter labelFitter = skipModeLabel.gameObject.AddComponent<UnityEngine.UI.ContentSizeFitter>();
            labelFitter.horizontalFit = UnityEngine.UI.ContentSizeFitter.FitMode.PreferredSize;

            // Help Button (?)
            GameObject skipHelpBtnObj = UIHelper.CreateUIObject("HelpButton", skipModeLabel.transform);
            RectTransform skipHelpRt = skipHelpBtnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(skipHelpRt, new Vector2(1, 0.5f), new Vector2(1, 0.5f), new Vector2(0, 0.5f));
            skipHelpRt.anchoredPosition = new Vector2(-5, 0); // -5px offset to account for internal padding
            skipHelpRt.sizeDelta = new Vector2(30, 30);
            UIHelper.AddImage(skipHelpBtnObj, new Color(0, 0, 0, 0)); // Invisible hit box
            Button skipHelpBtn = skipHelpBtnObj.AddComponent<Button>();
            skipHelpBtnObj.AddComponent<UIHoverSound>();
            GameObject skipHelpBtnTextObj = UIHelper.CreateUIObject("Text", skipHelpBtnObj.transform);
            RectTransform shtRt = skipHelpBtnTextObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(shtRt);
            Text skipHelpText = CreateLegacyText(skipHelpBtnTextObj, "?", HalloweenTheme.AccentOrange, 22, TextAnchor.MiddleCenter);
            skipHelpText.fontStyle = FontStyle.Bold;

            // The main dropdown button
            var skipTuple = CreateLegacyButton(panel.transform, "Ctrl ▼", 240, 40, new Color32(60, 40, 80, 255));
            RectTransform skipRt = skipTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(skipRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            skipRt.anchoredPosition = new Vector2(100, yPos);'''

# Dropdown Panel position adjustment
old_drop_panel = '''            RectTransform dropRt = dropPanelObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(dropRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            dropRt.anchoredPosition = new Vector2(0, yPos - 45 - 20 - 60);'''
new_drop_panel = '''            RectTransform dropRt = dropPanelObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(dropRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            dropRt.anchoredPosition = new Vector2(100, yPos - 20 - 60);'''

# Help Panel position
old_help_panel = '''            RectTransform shpRt = skipHelpPanelObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(shpRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            shpRt.anchoredPosition = new Vector2(0, yPos - 45 - 20 - 60); // same pos as drop panel'''
new_help_panel = '''            RectTransform shpRt = skipHelpPanelObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(shpRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            shpRt.anchoredPosition = new Vector2(100, yPos - 20 - 60); // same pos as drop panel'''

# 2. Update Font
old_font = '''            // 〓〓〓 4. Font Style (toggle button) 〓〓〓
            yPos -= 85;
            var fontStyleLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.font", "글꼴"), yPos);
            var fontTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.font_handwriting", "손글씨"), 220, 40, new Color32(60, 40, 80, 255));
            RectTransform fontRt = fontTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(fontRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            fontRt.anchoredPosition = new Vector2(0, yPos - 45);'''

new_font = '''            // 〓〓〓 4. Font Style (toggle button) 〓〓〓
            yPos -= 65;
            var fontStyleLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.font", "글꼴"), yPos);
            var fontTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.font_handwriting", "손글씨"), 240, 40, new Color32(60, 40, 80, 255));
            RectTransform fontRt = fontTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(fontRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            fontRt.anchoredPosition = new Vector2(100, yPos);'''

# 3. Update Flash
old_flash = '''            // 〓〓〓 5. Flash / Shake Effects (photosensitivity toggle) 〓〓〓
            yPos -= 85;
            var flashLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.flash_effect", "화면 번쩍임·흔들림"), yPos);
            var flashTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.flash_on", "켜짐"), 220, 40, new Color32(60, 40, 80, 255));
            RectTransform flashRt = flashTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(flashRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            flashRt.anchoredPosition = new Vector2(0, yPos - 45);'''

new_flash = '''            // 〓〓〓 5. Flash / Shake Effects (photosensitivity toggle) 〓〓〓
            yPos -= 65;
            var flashLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.flash_effect", "화면 번쩍임·흔들림"), yPos);
            var flashTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.flash_on", "켜짐"), 240, 40, new Color32(60, 40, 80, 255));
            RectTransform flashRt = flashTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(flashRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            flashRt.anchoredPosition = new Vector2(100, yPos);'''


# 4. Bottom Buttons
old_title_btn = '''            // 〓 Return to Title Button 〓
            var titleTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.return_to_title", "타이틀로 돌아가기"), 220, 44, new Color32(180, 50, 50, 255));
            RectTransform titleBtnRt = titleTuple.btn.GetComponent<RectTransform>();
            yPos -= 85;
            UIHelper.SetAnchors(titleBtnRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            titleBtnRt.anchoredPosition = new Vector2(0, yPos - 45);

            // --- Delete Data Button ---
            var deleteDataTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.delete_data", "데이터 삭제"), 220, 44, new Color32(180, 50, 50, 255));
            RectTransform deleteDataBtnRt = deleteDataTuple.btn.GetComponent<RectTransform>();
            yPos -= 60;
            UIHelper.SetAnchors(deleteDataBtnRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            deleteDataBtnRt.anchoredPosition = new Vector2(0, yPos - 45);'''

new_title_btn = '''            // 〓 Return to Title Button 〓
            var titleTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.return_to_title", "타이틀로 돌아가기"), 300, 44, new Color32(180, 50, 50, 255));
            RectTransform titleBtnRt = titleTuple.btn.GetComponent<RectTransform>();
            yPos -= 75; // More spacing before the bottom buttons
            UIHelper.SetAnchors(titleBtnRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            titleBtnRt.anchoredPosition = new Vector2(0, yPos);

            // --- Delete Data Button ---
            var deleteDataTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.delete_data", "데이터 삭제"), 300, 44, new Color32(180, 50, 50, 255));
            RectTransform deleteDataBtnRt = deleteDataTuple.btn.GetComponent<RectTransform>();
            yPos -= 55;
            UIHelper.SetAnchors(deleteDataBtnRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            deleteDataBtnRt.anchoredPosition = new Vector2(0, yPos);'''

content = content.replace(old_skip, new_skip)
content = content.replace(old_drop_panel, new_drop_panel)
content = content.replace(old_help_panel, new_help_panel)
content = content.replace(old_font, new_font)
content = content.replace(old_flash, new_flash)
content = content.replace(old_title_btn, new_title_btn)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated second half layout.")
