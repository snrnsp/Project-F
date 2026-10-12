import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = 'private void CreateSettingsUI()'
end_marker = 'private void CreateLanguageUI()'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_method = '''private void CreateSettingsUI()
        {
            settingsModalRoot = UIHelper.CreateUIObject("SettingsRoot", mainCanvas.transform);
            GameObject settingsRoot = settingsModalRoot;
            UIHelper.StretchFull(settingsRoot.GetComponent<RectTransform>());

            // Semi-transparent dark overlay (click to close)
            GameObject bgBtnObj = UIHelper.CreateUIObject("BackgroundButton", settingsRoot.transform);
            UIHelper.StretchFull(bgBtnObj.GetComponent<RectTransform>());
            UIHelper.AddImage(bgBtnObj, new Color(0, 0, 0, 0.7f));
            UnityEngine.UI.Button bgBtn = bgBtnObj.AddComponent<UnityEngine.UI.Button>();
            bgBtnObj.AddComponent<UIHoverSound>().playHover = false;
            bgBtn.transition = UnityEngine.UI.Selectable.Transition.None;

            // Settings panel
            GameObject panel = UIHelper.CreatePanel("SettingsPanel", settingsRoot.transform, HalloweenTheme.PanelBackground);
            UnityEngine.UI.Outline outline = panel.GetComponent<UnityEngine.UI.Outline>();
            if (outline != null) outline.effectDistance = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth + 4f);
            RectTransform panelRt = panel.GetComponent<RectTransform>();
            UIHelper.SetAnchors(panelRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            panelRt.sizeDelta = new Vector2(900, 750); // WIDER PANEL
            
            // Layout Group for the Panel
            VerticalLayoutGroup vlg = panel.AddComponent<VerticalLayoutGroup>();
            vlg.padding = new RectOffset(40, 40, 30, 30);
            vlg.spacing = 8;
            vlg.childControlWidth = true;
            vlg.childControlHeight = false;
            vlg.childForceExpandWidth = true;
            vlg.childForceExpandHeight = false;
            vlg.childAlignment = TextAnchor.UpperCenter;

            // Title
            GameObject titleObj = UIHelper.CreateUIObject("Title", panel.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            titleRt.sizeDelta = new Vector2(0, 50);
            Text titleText = CreateLegacyText(titleObj, Loc.Get("ui.builder.settings.title", "환경 설정"), HalloweenTheme.AccentOrange, 36, TextAnchor.MiddleCenter);

            // Helper to create rows
            GameObject CreateRow(string name, float height = 40) {
                GameObject row = UIHelper.CreateUIObject(name, panel.transform);
                RectTransform rowRt = row.GetComponent<RectTransform>();
                rowRt.sizeDelta = new Vector2(0, height);
                return row;
            }

            // 1. Text Speed
            GameObject tsRow = CreateRow("TextSpeedRow");
            var textSpeedLabel = CreateSettingsLabel(tsRow.transform, Loc.Get("ui.settings.text_speed", "텍스트 속도"), 0);
            textSpeedLabel.GetComponent<RectTransform>().anchoredPosition = new Vector2(-200, 0); // Offset from center
            Slider textSpeedSlider = CreateSettingsSlider(tsRow.transform, 0);
            textSpeedSlider.GetComponent<RectTransform>().anchoredPosition = new Vector2(100, 0);

            // Preview Text
            GameObject ptRow = CreateRow("PreviewTextRow", 30);
            Text previewText = CreateLegacyText(ptRow, "", HalloweenTheme.TextPrimary, 20, TextAnchor.MiddleCenter);
            previewText.GetComponent<RectTransform>().sizeDelta = new Vector2(800, 30);

            // 2. BGM
            GameObject bgmRow = CreateRow("BGMRow");
            var bgmVolumeLabel = CreateSettingsLabel(bgmRow.transform, Loc.Get("ui.settings.bgm_volume", "배경음악 (BGM) 음량"), 0);
            bgmVolumeLabel.GetComponent<RectTransform>().anchoredPosition = new Vector2(-200, 0);
            Slider bgmVolumeSlider = CreateSettingsSlider(bgmRow.transform, 0);
            bgmVolumeSlider.GetComponent<RectTransform>().anchoredPosition = new Vector2(100, 0);
            Text bgmVolumeValueText = CreateSettingsValueText(bgmRow.transform, 0);
            bgmVolumeValueText.GetComponent<RectTransform>().anchoredPosition = new Vector2(300, 0);

            // 3. SFX
            GameObject sfxRow = CreateRow("SFXRow");
            var sfxVolumeLabel = CreateSettingsLabel(sfxRow.transform, Loc.Get("ui.settings.sfx_volume", "효과음 (SFX) 음량"), 0);
            sfxVolumeLabel.GetComponent<RectTransform>().anchoredPosition = new Vector2(-200, 0);
            Slider sfxVolumeSlider = CreateSettingsSlider(sfxRow.transform, 0);
            sfxVolumeSlider.GetComponent<RectTransform>().anchoredPosition = new Vector2(100, 0);
            Text sfxVolumeValueText = CreateSettingsValueText(sfxRow.transform, 0);
            sfxVolumeValueText.GetComponent<RectTransform>().anchoredPosition = new Vector2(300, 0);

            // 4. Auto Play
            GameObject autoRow = CreateRow("AutoPlayRow");
            var autoPlayLabel = CreateSettingsLabel(autoRow.transform, Loc.Get("ui.settings.auto_play_delay", "오토 대기 시간"), 0);
            autoPlayLabel.GetComponent<RectTransform>().anchoredPosition = new Vector2(-200, 0);
            Slider autoPlaySlider = CreateSettingsSlider(autoRow.transform, 0);
            autoPlaySlider.GetComponent<RectTransform>().anchoredPosition = new Vector2(100, 0);
            
            GameObject inputTextObj = UIHelper.CreateUIObject("InputField", autoRow.transform);
            RectTransform inputTextRt = inputTextObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(inputTextRt, new Vector2(0.5f, 1f), new Vector2(0.5f, 1f), new Vector2(0.5f, 1f));
            inputTextRt.anchoredPosition = new Vector2(300, 0);
            inputTextRt.sizeDelta = new Vector2(70, 30);
            UIHelper.AddImage(inputTextObj, new Color32(0, 0, 0, 255));
            UnityEngine.UI.Outline inputOutline = inputTextObj.AddComponent<UnityEngine.UI.Outline>();
            inputOutline.effectColor = HalloweenTheme.AccentOrange;
            InputField autoPlayInputField = inputTextObj.AddComponent<InputField>();
            Text autoPlayValueText = CreateLegacyText(inputTextObj, "2.0", new Color32(255, 255, 255, 255), 20, TextAnchor.MiddleCenter);
            autoPlayValueText.GetComponent<RectTransform>().sizeDelta = new Vector2(70, 30);
            autoPlayInputField.textComponent = autoPlayValueText;

            // 5. Skip Mode
            GameObject skipRow = CreateRow("SkipRow");
            var skipModeLabel = CreateSettingsLabel(skipRow.transform, Loc.Get("ui.builder.settings.skip_key", "스킵 모드"), 0);
            skipModeLabel.GetComponent<RectTransform>().anchoredPosition = new Vector2(-200, 0);
            
            GameObject skipHelpBtnObj = UIHelper.CreateUIObject("HelpButton", skipRow.transform);
            RectTransform skipHelpRt = skipHelpBtnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(skipHelpRt, new Vector2(0.5f, 1f), new Vector2(0.5f, 1f), new Vector2(0.5f, 1f));
            skipHelpRt.anchoredPosition = new Vector2(-15, 0);
            skipHelpRt.sizeDelta = new Vector2(30, 30);
            UIHelper.AddImage(skipHelpBtnObj, new Color(0, 0, 0, 0));
            Button skipHelpBtn = skipHelpBtnObj.AddComponent<Button>();
            skipHelpBtnObj.AddComponent<UIHoverSound>();
            Text skipHelpTextBtn = CreateLegacyText(skipHelpBtnObj, "?", HalloweenTheme.AccentOrange, 22, TextAnchor.MiddleCenter);
            skipHelpTextBtn.fontStyle = FontStyle.Bold;
            skipHelpTextBtn.GetComponent<RectTransform>().sizeDelta = new Vector2(30, 30);

            var skipTuple = CreateLegacyButton(skipRow.transform, "Ctrl ▼", 240, 40, new Color32(60, 40, 80, 255));
            skipTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(100, 0);

            // Skip Dropdown Panel (Will be positioned absolutely later to avoid layout groups)
            GameObject dropPanelObj = UIHelper.CreateUIObject("SkipDropdown", settingsRoot.transform);
            RectTransform dropRt = dropPanelObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(dropRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            dropRt.anchoredPosition = new Vector2(100, 10);
            dropRt.sizeDelta = new Vector2(240, 120);
            UIHelper.AddImage(dropPanelObj, new Color32(30, 20, 40, 255));
            UnityEngine.UI.Outline dropOut = dropPanelObj.AddComponent<UnityEngine.UI.Outline>();
            dropOut.effectColor = HalloweenTheme.AccentOrange;
            VerticalLayoutGroup dropVlg = dropPanelObj.AddComponent<VerticalLayoutGroup>();
            dropVlg.childControlHeight = true; dropVlg.childControlWidth = true;
            
            var optCtrl = CreateLegacyButton(dropPanelObj.transform, "Ctrl", 240, 40, new Color32(50, 35, 70, 255));
            optCtrl.text.fontSize = 20;
            var optShift = CreateLegacyButton(dropPanelObj.transform, "Shift", 240, 40, new Color32(50, 35, 70, 255));
            optShift.text.fontSize = 20;
            var optSpace = CreateLegacyButton(dropPanelObj.transform, "Space", 240, 40, new Color32(50, 35, 70, 255));
            optSpace.text.fontSize = 20;
            dropPanelObj.SetActive(false);

            // Skip Help Panel (Absolute positioning)
            GameObject skipHelpPanelObj = UIHelper.CreateUIObject("SkipHelpPanel", settingsRoot.transform);
            RectTransform shpRt = skipHelpPanelObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(shpRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            shpRt.anchoredPosition = new Vector2(100, 10);
            shpRt.sizeDelta = new Vector2(400, 60);
            UIHelper.AddImage(skipHelpPanelObj, new Color32(20, 15, 30, 250));
            UnityEngine.UI.Outline shpOut = skipHelpPanelObj.AddComponent<UnityEngine.UI.Outline>();
            shpOut.effectColor = HalloweenTheme.AccentOrange;
            Text skipHelpPanelText = CreateLegacyText(skipHelpPanelObj, Loc.Get("ui.settings.skip_desc", "설정하신 단축키를 누르고 있으면 대사를 빠르게 넘길 수 있습니다."), new Color32(200, 190, 210, 255), 18, TextAnchor.MiddleCenter);
            skipHelpPanelText.GetComponent<RectTransform>().sizeDelta = new Vector2(380, 50);
            skipHelpPanelObj.SetActive(false);

            // 6. Font Style
            GameObject fontRow = CreateRow("FontRow");
            var fontStyleLabel = CreateSettingsLabel(fontRow.transform, Loc.Get("ui.settings.font", "글꼴"), 0);
            fontStyleLabel.GetComponent<RectTransform>().anchoredPosition = new Vector2(-200, 0);
            var fontTuple = CreateLegacyButton(fontRow.transform, Loc.Get("ui.settings.font_handwriting", "손글씨"), 240, 40, new Color32(60, 40, 80, 255));
            fontTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(100, 0);
            fontTuple.text.fontSize = 20;

            // 7. Flash
            GameObject flashRow = CreateRow("FlashRow");
            var flashLabel = CreateSettingsLabel(flashRow.transform, Loc.Get("ui.settings.flash_effect", "화면 번쩍임.흔들림"), 0);
            flashLabel.GetComponent<RectTransform>().anchoredPosition = new Vector2(-200, 0);
            var flashTuple = CreateLegacyButton(flashRow.transform, Loc.Get("ui.settings.flash_on", "켜짐"), 240, 40, new Color32(60, 40, 80, 255));
            flashTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(100, 0);
            flashTuple.text.fontSize = 20;

            // Spacer
            CreateRow("Spacer", 20);

            // 8. Return to Title
            GameObject titleBtnRow = CreateRow("TitleBtnRow", 50);
            var titleTuple = CreateLegacyButton(titleBtnRow.transform, Loc.Get("ui.settings.return_to_title", "타이틀로 돌아가기"), 300, 44, new Color32(180, 50, 50, 255));
            titleTuple.btn.GetComponent<RectTransform>().anchoredPosition = Vector2.zero;

            // 9. Delete Data
            GameObject deleteBtnRow = CreateRow("DeleteBtnRow", 50);
            var deleteDataTuple = CreateLegacyButton(deleteBtnRow.transform, Loc.Get("ui.settings.delete_data", "데이터 삭제"), 300, 44, new Color32(180, 50, 50, 255));
            deleteDataTuple.btn.GetComponent<RectTransform>().anchoredPosition = Vector2.zero;

            // Close Button
            var closeTuple = CreateLegacyButton(settingsRoot.transform, "X", 44, 44, new Color32(180, 50, 50, 255));
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            closeRt.anchoredPosition = new Vector2(420, 340); // Top right of the 900x750 panel
            closeTuple.text.fontSize = 26;
            closeTuple.text.fontStyle = FontStyle.Bold;

            // Attach SettingsUI
            SettingsUI settingsUi = settingsRoot.AddComponent<SettingsUI>();
            settingsUiRef = settingsUi;
            bgBtn.onClick.AddListener(() => settingsUi.Hide());
            if (globalMgrRef != null) globalMgrRef.Initialize(settingsRoot);
            UIHelper.SetField(settingsUi, "settingsPanel", settingsRoot);
            UIHelper.SetField(settingsUi, "titleTextLabel", titleText);
            UIHelper.SetField(settingsUi, "bgmVolumeSlider", bgmVolumeSlider);
            UIHelper.SetField(settingsUi, "bgmVolumeLabel", bgmVolumeLabel);
            UIHelper.SetField(settingsUi, "sfxVolumeSlider", sfxVolumeSlider);
            UIHelper.SetField(settingsUi, "sfxVolumeLabel", sfxVolumeLabel);
            UIHelper.SetField(settingsUi, "bgmVolumeValueText", bgmVolumeValueText);
            UIHelper.SetField(settingsUi, "sfxVolumeValueText", sfxVolumeValueText);
            UIHelper.SetField(settingsUi, "textSpeedSlider", textSpeedSlider);
            UIHelper.SetField(settingsUi, "textSpeedLabel", textSpeedLabel);
            UIHelper.SetField(settingsUi, "previewTextLabel", previewText);
            UIHelper.SetField(settingsUi, "autoPlaySlider", autoPlaySlider);
            UIHelper.SetField(settingsUi, "autoPlayLabel", autoPlayLabel);
            UIHelper.SetField(settingsUi, "autoPlayInputField", autoPlayInputField);
            UIHelper.SetField(settingsUi, "fontStyleButton", fontTuple.btn);
            UIHelper.SetField(settingsUi, "fontStyleLabel", fontStyleLabel);
            UIHelper.SetField(settingsUi, "fontStyleValueText", fontTuple.text);
            UIHelper.SetField(settingsUi, "closeButton", closeTuple.btn);
            UIHelper.SetField(settingsUi, "returnToTitleButton", titleTuple.btn);
            UIHelper.SetField(settingsUi, "returnToTitleLabel", titleTuple.text);
            UIHelper.SetField(settingsUi, "deleteDataButton", deleteDataTuple.btn);
            UIHelper.SetField(settingsUi, "flashEffectLabel", flashLabel);
            UIHelper.SetField(settingsUi, "flashEffectButton", flashTuple.btn);
            UIHelper.SetField(settingsUi, "flashEffectValueText", flashTuple.text);

            UIHelper.SetField(settingsUi, "ctrlSkipButton", skipTuple.btn);
            UIHelper.SetField(settingsUi, "skipModeLabel", skipModeLabel);
            UIHelper.SetField(settingsUi, "skipHelpButton", skipHelpBtn);
            UIHelper.SetField(settingsUi, "skipHelpPanel", skipHelpPanelObj);
            UIHelper.SetField(settingsUi, "skipHelpText", skipHelpPanelText);
            UIHelper.SetField(settingsUi, "ctrlSkipValueText", skipTuple.text);
            UIHelper.SetField(settingsUi, "skipDropdownPanel", dropPanelObj);
            UIHelper.SetField(settingsUi, "skipOptCtrl", optCtrl.btn);
            UIHelper.SetField(settingsUi, "skipOptShift", optShift.btn);
            UIHelper.SetField(settingsUi, "skipOptSpace", optSpace.btn);
            
            settingsRoot.SetActive(false);
        }
        
        '''
    content = content[:start_idx] + new_method + content[end_idx:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Rewrote SettingsUI with a flexible VerticalLayoutGroup up to CreateLanguageUI!")
