import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find and replace the entire CreateExtraUI method
start_marker = '        private void CreateExtraUI()\n        {'
end_marker = '        private void CreateGlobalUI()'

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print('Could not find method boundaries')
    exit()

new_method = '''        private void CreateExtraUI()
        {
            // Root panel (fullscreen overlay, starts hidden)
            GameObject extraRoot = UIHelper.CreateUIObject("ExtraPanel", mainCanvas.transform);
            UIHelper.StretchFull(extraRoot.GetComponent<RectTransform>());
            extraRoot.SetActive(false);

            // Dark background (click to close)
            GameObject extraBgBtnObj = UIHelper.CreateUIObject("BackgroundButton", extraRoot.transform);
            UIHelper.StretchFull(extraBgBtnObj.GetComponent<RectTransform>());
            UIHelper.AddImage(extraBgBtnObj, new Color32(15, 8, 25, 200));
            UnityEngine.UI.Button extraBgBtn = extraBgBtnObj.AddComponent<UnityEngine.UI.Button>();
            extraBgBtn.transition = UnityEngine.UI.Selectable.Transition.None;

            // ===== Header =====
            GameObject headerObj = UIHelper.CreateUIObject("Header", extraRoot.transform);
            RectTransform headerRt = headerObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(headerRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0.5f, 1));
            headerRt.anchoredPosition = new Vector2(0, -20);
            headerRt.sizeDelta = new Vector2(0, 60);
            // Raycast blocker for header area
            UIHelper.AddImage(headerObj, new Color(0, 0, 0, 0));

            GameObject titleObj = UIHelper.CreateUIObject("Title", headerObj.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            titleRt.sizeDelta = new Vector2(400, 50);
            UIHelper.AddText(titleObj, "\\uce90\\ub9ad\\ud130 \\uc124\\uc815\\uc9d1", new Color32(210, 185, 140, 255), 30, TextAlignmentOptions.Center);

            // ===== Close Button =====
            GameObject closeBtnObj = UIHelper.CreateUIObject("CloseBtn", headerObj.transform);
            RectTransform closeRt = closeBtnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(1, 0.5f), new Vector2(1, 0.5f), new Vector2(1, 0.5f));
            closeRt.anchoredPosition = new Vector2(-40, 0);
            closeRt.sizeDelta = new Vector2(40, 40);
            Image closeBtnImg = UIHelper.AddImage(closeBtnObj, Color.white);
            closeBtnImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, new Color32(180, 50, 50, 255), new Color32(255, 120, 120, 255));
            closeBtnImg.type = Image.Type.Sliced;
            Button closeBtn = closeBtnObj.AddComponent<Button>();

            GameObject closeTextObj = UIHelper.CreateUIObject("Text", closeBtnObj.transform);
            RectTransform textRt = closeTextObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(textRt);
            textRt.offsetMin = new Vector2(0, 2);
            textRt.offsetMax = new Vector2(0, 2);
            UIHelper.AddText(closeTextObj, "X", Color.white, 24, TextAlignmentOptions.Center);

            // ===== Back shadow box (simulates folder stack depth) =====
            GameObject shadowBox = UIHelper.CreateUIObject("ShadowBox", extraRoot.transform);
            RectTransform shadowRt = shadowBox.GetComponent<RectTransform>();
            UIHelper.SetAnchors(shadowRt, new Vector2(0, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
            shadowRt.offsetMin = new Vector2(35, 15);
            shadowRt.offsetMax = new Vector2(-15, -80);
            Image shadowImg = UIHelper.AddImage(shadowBox, new Color32(80, 60, 40, 255));
            shadowImg.sprite = UIHelper.CreateRoundedRectSprite(10, 2, new Color32(80, 60, 40, 255), new Color32(60, 45, 25, 255));
            shadowImg.type = Image.Type.Sliced;

            // ===== Create 6 Folder objects =====
            string[] charNames = { "\\uc138\\uc774\\uce74", "\\uce74\\uc2a4\\ubbf8", "\\ub9ac\\ub098", "\\ub9ac\\ub9ac\\uc2a4", "\\ubbf8\\ub098", "\\ud558\\ub8e8\\uce74" };
            int folderCount = charNames.Length;

            // Folder colors
            Color32 folderBorder = new Color32(90, 65, 35, 255);
            Color32 folderBodyDefault = new Color32(210, 185, 140, 255);

            ExtraUI extraUi = extraRoot.AddComponent<ExtraUI>();
            extraBgBtn.onClick.AddListener(() => extraUi.Hide());
            UIHelper.SetField(extraUi, "extraPanel", extraRoot);
            UIHelper.SetField(extraUi, "globalSettingsButton", globalSettingsBtnObj);
            UIHelper.SetField(extraUi, "lobbySettingsButton", lobbySettingsBtnObj);
            UIHelper.SetField(extraUi, "closeButton", closeBtn);

            for (int ci = 0; ci < folderCount; ci++)
            {
                // ===== Folder Root =====
                GameObject folder = UIHelper.CreateUIObject("Folder_" + charNames[ci], extraRoot.transform);
                RectTransform folderRt = folder.GetComponent<RectTransform>();
                UIHelper.SetAnchors(folderRt, new Vector2(0, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
                folderRt.offsetMin = new Vector2(40, 20);
                folderRt.offsetMax = new Vector2(-20, -85);

                // ===== Tab (upper protruding part of the folder) =====
                float tabFraction = 1f / folderCount;
                float tabLeft = tabFraction * ci;
                float tabRight = tabFraction * (ci + 1);

                GameObject tabObj = UIHelper.CreateUIObject("Tab", folder.transform);
                RectTransform tabRt = tabObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(tabRt, new Vector2(tabLeft, 1), new Vector2(tabRight, 1), new Vector2(0.5f, 1));
                tabRt.anchoredPosition = new Vector2(0, 35);
                tabRt.sizeDelta = new Vector2(-6, 35);

                // Tab image with rounded top corners
                Image tabImg = UIHelper.AddImage(tabObj, folderBodyDefault);
                tabImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, Color.white, folderBorder);
                tabImg.type = Image.Type.Sliced;

                // Tab text
                GameObject tabTextObj = UIHelper.CreateUIObject("Text", tabObj.transform);
                UIHelper.StretchFull(tabTextObj.GetComponent<RectTransform>());
                TextMeshProUGUI tabText = UIHelper.AddText(tabTextObj, charNames[ci], new Color32(60, 40, 20, 255), 18, TextAlignmentOptions.Center);
                tabText.fontStyle = FontStyles.Bold;

                // Tab click handler
                Button tabBtn = tabObj.AddComponent<Button>();
                tabBtn.transition = Selectable.Transition.None;
                int capturedIndex = ci;
                tabBtn.onClick.AddListener(() => { extraUi.SelectCharacter(capturedIndex); });

                // ===== Body (main content area) =====
                GameObject bodyObj = UIHelper.CreateUIObject("Body", folder.transform);
                RectTransform bodyRt = bodyObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(bodyRt);

                Image bodyImg = UIHelper.AddImage(bodyObj, folderBodyDefault);
                bodyImg.sprite = UIHelper.CreateRoundedRectSprite(10, 2, Color.white, folderBorder);
                bodyImg.type = Image.Type.Sliced;

                // ===== Portrait (left side) =====
                GameObject portraitObj = UIHelper.CreateUIObject("Portrait", bodyObj.transform);
                RectTransform portraitRt = portraitObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(portraitRt, new Vector2(0, 0), new Vector2(0.32f, 1), new Vector2(0.5f, 0.5f));
                portraitRt.offsetMin = new Vector2(30, 60);
                portraitRt.offsetMax = new Vector2(-20, -100);
                Image portraitImg = UIHelper.AddImage(portraitObj, new Color(1, 1, 1, 0));
                portraitImg.preserveAspect = true;

                // ===== Info panel (right side with scroll) =====
                GameObject infoPanelObj = UIHelper.CreateUIObject("Scroll", bodyObj.transform);
                RectTransform infoPanelRt = infoPanelObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(infoPanelRt, new Vector2(0.32f, 0), new Vector2(1, 1), new Vector2(0.5f, 0.5f));
                infoPanelRt.offsetMin = new Vector2(5, 10);
                infoPanelRt.offsetMax = new Vector2(-15, -10);

                ScrollRect scrollRect = infoPanelObj.AddComponent<ScrollRect>();
                scrollRect.horizontal = false;
                scrollRect.vertical = true;
                scrollRect.movementType = ScrollRect.MovementType.Clamped;
                UIHelper.AddImage(infoPanelObj, new Color(0, 0, 0, 0));

                // Viewport
                GameObject viewportObj = UIHelper.CreateUIObject("Viewport", infoPanelObj.transform);
                UIHelper.StretchFull(viewportObj.GetComponent<RectTransform>());
                viewportObj.AddComponent<RectMask2D>();

                // Content
                GameObject contentObj = UIHelper.CreateUIObject("Content", viewportObj.transform);
                RectTransform contentRt = contentObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(contentRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0, 1));
                contentRt.sizeDelta = new Vector2(0, 0);
                ContentSizeFitter fitter = contentObj.AddComponent<ContentSizeFitter>();
                fitter.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

                scrollRect.viewport = viewportObj.GetComponent<RectTransform>();
                scrollRect.content = contentRt;

                // Name text
                GameObject nameObj = UIHelper.CreateUIObject("NameText", contentObj.transform);
                RectTransform nameRt = nameObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(nameRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0, 1));
                nameRt.sizeDelta = new Vector2(0, 50);
                TextMeshProUGUI nameText = UIHelper.AddText(nameObj, "", new Color32(60, 40, 20, 255), 28, TextAlignmentOptions.Left);
                nameText.fontStyle = FontStyles.Bold;
                nameText.margin = new Vector4(20, 20, 20, 0);

                // Profile text
                GameObject profileObj = UIHelper.CreateUIObject("ProfileText", contentObj.transform);
                RectTransform profileRt = profileObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(profileRt, new Vector2(0, 1), new Vector2(1, 1), new Vector2(0, 1));
                profileRt.sizeDelta = new Vector2(0, 0);
                TextMeshProUGUI profileText = UIHelper.AddText(profileObj, "", new Color32(50, 40, 30, 255), 18, TextAlignmentOptions.TopLeft);
                profileText.textWrappingMode = TextWrappingModes.Normal;
                profileText.margin = new Vector4(20, 10, 20, 40);
                profileText.lineSpacing = 8f;

                // Layout
                VerticalLayoutGroup vlg = contentObj.AddComponent<VerticalLayoutGroup>();
                vlg.childForceExpandWidth = true;
                vlg.childForceExpandHeight = false;
                vlg.childControlWidth = true;
                vlg.childControlHeight = true;
                vlg.padding = new RectOffset(0, 0, 10, 20);

                LayoutElement profileLE = profileObj.AddComponent<LayoutElement>();
                profileLE.flexibleWidth = 1;
                LayoutElement nameLE = nameObj.AddComponent<LayoutElement>();
                nameLE.minHeight = 50;
                nameLE.flexibleWidth = 1;

                // Register folder with ExtraUI
                extraUi.RegisterFolder(folder, bodyImg, tabImg, tabText);
            }

            extraUiRef = extraUi;
        }

'''

text = text[:start_idx] + new_method + '        ' + text[end_idx:]

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('CreateExtraUI rewritten with folder-style UI')
