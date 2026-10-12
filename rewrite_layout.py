import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace everything from loat yPos = -135; down to // Attach SettingsUI
start_marker = "float yPos = -135;"
end_marker = "// Attach SettingsUI"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find markers!")
    sys.exit(1)

new_block = '''float yPos = -100;

            // 〓〓〓 1. Text Speed 〓〓〓
            var textSpeedLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.text_speed", "텍스트 속도"), yPos);
            Slider textSpeedSlider = CreateSettingsSlider(panel.transform, yPos);

            // Preview Text & Background (to see opacity)
            yPos -= 50;
            // The Text (No background needed anymore since Opacity setting is gone)
            GameObject previewTextObj = UIHelper.CreateUIObject("PreviewText", panel.transform);
            RectTransform ptextRt = previewTextObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(ptextRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            ptextRt.anchoredPosition = new Vector2(0, yPos);
            ptextRt.sizeDelta = new Vector2(620, 60);
            Text previewText = CreateLegacyText(previewTextObj, "", HalloweenTheme.TextPrimary, 24, TextAnchor.MiddleCenter);

            yPos -= 65;

            // 〓〓〓 BGM Volume 〓〓〓
            var bgmVolumeLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.bgm_volume", "배경음악 (BGM) 음량"), yPos);
            Slider bgmVolumeSlider = CreateSettingsSlider(panel.transform, yPos);
            Text bgmVolumeValueText = CreateSettingsValueText(panel.transform, yPos);
            
            yPos -= 60;

            // 〓〓〓 SFX Volume 〓〓〓
            var sfxVolumeLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.sfx_volume", "효과음 (SFX) 음량"), yPos);
            Slider sfxVolumeSlider = CreateSettingsSlider(panel.transform, yPos);
            Text sfxVolumeValueText = CreateSettingsValueText(panel.transform, yPos);

            // 〓〓〓 2. Auto-play Delay 〓〓〓
            yPos -= 60;
            var autoPlayLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.auto_play_delay", "오토 대기 시간"), yPos);
            Slider autoPlaySlider = CreateSettingsSlider(panel.transform, yPos);

            // Value InputField (right side of slider)
            GameObject autoValObj = UIHelper.CreateUIObject("AutoPlayValue", panel.transform);
            RectTransform autoValRt = autoValObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(autoValRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            autoValRt.anchoredPosition = new Vector2(260, yPos);
            autoValRt.sizeDelta = new Vector2(70, 30);

            UnityEngine.UI.Image inputBg = UIHelper.AddImage(autoValObj, new Color32(0, 0, 0, 255));
            UnityEngine.UI.Outline inputOutline = autoValObj.AddComponent<UnityEngine.UI.Outline>();
            inputOutline.effectColor = HalloweenTheme.AccentOrange;
            inputOutline.effectDistance = new Vector2(2, -2);

            UnityEngine.UI.InputField autoPlayInputField = autoValObj.AddComponent<UnityEngine.UI.InputField>();
            autoPlayInputField.transition = UnityEngine.UI.Selectable.Transition.ColorTint;
            autoPlayInputField.characterValidation = UnityEngine.UI.InputField.CharacterValidation.Decimal;

            GameObject inputTextObj = UIHelper.CreateUIObject("Text", autoValObj.transform);
            RectTransform inputTextRt = inputTextObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(inputTextRt);
            inputTextRt.offsetMin = new Vector2(0, 0);
            inputTextRt.offsetMax = new Vector2(0, 0);
            Text autoPlayValueText = CreateLegacyText(inputTextObj, "2.0", new Color32(255, 255, 255, 255), 20, TextAnchor.MiddleCenter);
            autoPlayInputField.textComponent = autoPlayValueText;
            
            // 〓〓〓 3. Skip Mode (Dropdown) 〓〓〓
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
            skipRt.anchoredPosition = new Vector2(100, yPos);

            // Dropdown Panel
            GameObject dropPanelObj = UIHelper.CreateUIObject("SkipDropdown", panel.transform);
            RectTransform dropRt = dropPanelObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(dropRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            dropRt.anchoredPosition = new Vector2(100, yPos - 20 - 60);
            dropRt.sizeDelta = new Vector2(240, 120);
            UIHelper.AddImage(dropPanelObj, new Color32(30, 20, 40, 255));
            UnityEngine.UI.Outline dropOut = dropPanelObj.AddComponent<UnityEngine.UI.Outline>();
            dropOut.effectColor = HalloweenTheme.AccentOrange;
            
            // Layout Group for dropdown
            UnityEngine.UI.VerticalLayoutGroup vlg = dropPanelObj.AddComponent<UnityEngine.UI.VerticalLayoutGroup>();
            vlg.childControlHeight = true; vlg.childControlWidth = true;
            
            var optCtrl = CreateLegacyButton(dropPanelObj.transform, "Ctrl", 240, 40, new Color32(50, 35, 70, 255));
            optCtrl.text.fontSize = 20;
            var optShift = CreateLegacyButton(dropPanelObj.transform, "Shift", 240, 40, new Color32(50, 35, 70, 255));
            optShift.text.fontSize = 20;
            var optSpace = CreateLegacyButton(dropPanelObj.transform, "Space", 240, 40, new Color32(50, 35, 70, 255));
            optSpace.text.fontSize = 20;

            // Help Panel (Initially hidden)
            GameObject skipHelpPanelObj = UIHelper.CreateUIObject("SkipHelpPanel", panel.transform);
            RectTransform shpRt = skipHelpPanelObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(shpRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            shpRt.anchoredPosition = new Vector2(0, yPos - 30); // Centered below skip row
            shpRt.sizeDelta = new Vector2(400, 60);
            UIHelper.AddImage(skipHelpPanelObj, new Color32(20, 15, 30, 250));
            UnityEngine.UI.Outline shpOut = skipHelpPanelObj.AddComponent<UnityEngine.UI.Outline>();
            shpOut.effectColor = HalloweenTheme.AccentOrange;
            
            GameObject shtpObj = UIHelper.CreateUIObject("Text", skipHelpPanelObj.transform);
            RectTransform shtpRt = shtpObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(shtpRt);
            shtpRt.offsetMin = new Vector2(10, 5); shtpRt.offsetMax = new Vector2(-10, -5);
            Text skipHelpPanelText = CreateLegacyText(shtpObj, Loc.Get("ui.settings.skip_desc", "설정된 키를 누르고 있으면 대사를 빠르게 넘깁니다."), HalloweenTheme.TextSecondary, 18, TextAnchor.MiddleCenter);

            // 〓〓〓 4. Font Style (toggle button) 〓〓〓
            yPos -= 65;
            var fontStyleLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.font", "글꼴"), yPos);
            var fontTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.font_handwriting", "손글씨"), 240, 40, new Color32(60, 40, 80, 255));
            RectTransform fontRt = fontTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(fontRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            fontRt.anchoredPosition = new Vector2(100, yPos);
            fontTuple.text.fontSize = 20;

            // 〓〓〓 5. Flash / Shake Effects (photosensitivity toggle) 〓〓〓
            yPos -= 65;
            var flashLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.flash_effect", "화면 번쩍임·흔들림"), yPos);
            var flashTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.flash_on", "켜짐"), 240, 40, new Color32(60, 40, 80, 255));
            RectTransform flashRt = flashTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(flashRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            flashRt.anchoredPosition = new Vector2(100, yPos);
            flashTuple.text.fontSize = 20;

            // 〓〓〓 Close Button 〓〓〓
            var closeTuple = CreateLegacyButton(panel.transform, "X", 44, 44, new Color32(180, 50, 50, 255));
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            closeRt.anchoredPosition = new Vector2(-40, -40);
            closeTuple.text.fontSize = 26;
            closeTuple.text.fontStyle = FontStyle.Bold;

            // 〓 Return to Title Button 〓
            yPos -= 80;
            var titleTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.return_to_title", "타이틀로 돌아가기"), 300, 44, new Color32(180, 50, 50, 255));
            RectTransform titleBtnRt = titleTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleBtnRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            titleBtnRt.anchoredPosition = new Vector2(0, yPos);

            // --- Delete Data Button ---
            yPos -= 60;
            var deleteDataTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.delete_data", "데이터 삭제"), 300, 44, new Color32(180, 50, 50, 255));
            RectTransform deleteDataBtnRt = deleteDataTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(deleteDataBtnRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            deleteDataBtnRt.anchoredPosition = new Vector2(0, yPos);

            '''

content = content[:start_idx] + new_block + content[end_idx:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Complete Settings layout rewrite.")
