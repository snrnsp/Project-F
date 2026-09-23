import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

# 1. Modify OnNewGameClicked
target_newgame = '''        private void OnNewGameClicked()
        {
            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
            ShowPhotosensitivityWarning();
        }'''

replacement_newgame = '''        private void OnNewGameClicked()
        {
            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
            ShowPreAlphaWarning();
        }'''

# 2. Add ShowPreAlphaWarning before ShowPhotosensitivityWarning
idx = text.find('private void ShowPhotosensitivityWarning()')
pre_alpha_method = '''
        private void ShowPreAlphaWarning()
        {
            GameObject overlay = new GameObject("PreAlphaOverlay");
            overlay.transform.SetParent(lobbyPanel.transform.parent, false);
            RectTransform overlayRt = overlay.AddComponent<RectTransform>();
            overlayRt.anchorMin = Vector2.zero;
            overlayRt.anchorMax = Vector2.one;
            overlayRt.offsetMin = Vector2.zero;
            overlayRt.offsetMax = Vector2.zero;
            Image overlayImg = overlay.AddComponent<Image>();
            overlayImg.color = new Color(0, 0, 0, 0.85f);
            
            Button overlayBtn = overlay.AddComponent<Button>();
            overlayBtn.transition = Selectable.Transition.None;
            overlayBtn.onClick.AddListener(() => {
                Destroy(overlay);
            });

            GameObject panel = new GameObject("WarningPanel");
            panel.transform.SetParent(overlay.transform, false);
            RectTransform panelRt = panel.AddComponent<RectTransform>();
            panelRt.anchorMin = new Vector2(0.5f, 0.5f);
            panelRt.anchorMax = new Vector2(0.5f, 0.5f);
            panelRt.sizeDelta = new Vector2(820, 450);
            Image panelImg = panel.AddComponent<Image>();
            panelImg.type = Image.Type.Sliced;
            panelImg.sprite = CreateRoundedRectSprite(16, 2, new Color32(25, 20, 35, 255), new Color32(100, 180, 255, 255));
            
            Button panelDummyBtn = panel.AddComponent<Button>();
            panelDummyBtn.transition = Selectable.Transition.None;

            float titleY = -60f;

            GameObject iconObj = new GameObject("PreAlphaTitle");
            iconObj.transform.SetParent(panel.transform, false);
            RectTransform iconRt = iconObj.AddComponent<RectTransform>();
            iconRt.anchorMin = new Vector2(0.5f, 1f);
            iconRt.anchorMax = new Vector2(0.5f, 1f);
            iconRt.anchoredPosition = new Vector2(0, titleY);
            iconRt.sizeDelta = new Vector2(500, 45);
            TextMeshProUGUI iconText = Theme.UIHelper.AddText(iconObj, "Pre-Alpha \uc548\ub0b4", new Color32(150, 200, 255, 255), 30, TextAlignmentOptions.Center);
            iconText.fontStyle = FontStyles.Bold;

            GameObject msgObj = new GameObject("WarningMessage");
            msgObj.transform.SetParent(panel.transform, false);
            RectTransform msgRt = msgObj.AddComponent<RectTransform>();
            msgRt.anchorMin = new Vector2(0.5f, 1f);
            msgRt.anchorMax = new Vector2(0.5f, 1f);
            msgRt.anchoredPosition = new Vector2(0, -180);
            msgRt.sizeDelta = new Vector2(720, 200);
            
            string preAlphaMsg = "\ud604\uc7ac \uc624\ube14\ub9ac\ube44\uc5b8\uc740 '<color=#80C0FF>\ud504\ub9ac \uc54c\ud30c</color>(\uc18c\ud504\ud2b8\uc6e8\uc5b4\ub098 \uac8c\uc784 \uac1c\ubc1c \uacfc\uc815\uc5d0\uc11c \uc815\uc2dd \uc54c\ud30c \ud14c\uc2a4\ud2b8 \uc774\uc804\uc758 \ucd08\uae30 \uc81c\uc791 \ubc0f \uc124\uacc4 \ub2e8\uacc4)'\uc5d0 \uc788\uc2b5\ub2c8\ub2e4!\n\n\uac8c\uc784\uc758 \ud488\uc9c8\uc774 \ub0ae\uc744 \uc218 \uc788\ub294 \uc810 \uc591\ud574 \ubc14\ub78d\ub2c8\ub2e4!";
            
            TextMeshProUGUI msgText = Theme.UIHelper.AddText(msgObj, preAlphaMsg, new Color32(230, 230, 230, 255), 24, TextAlignmentOptions.Center);
            msgText.lineSpacing = 15f;

            GameObject btnObj = new GameObject("OkButton");
            btnObj.transform.SetParent(panel.transform, false);
            RectTransform btnRt = btnObj.AddComponent<RectTransform>();
            btnRt.anchorMin = new Vector2(0.5f, 0f);
            btnRt.anchorMax = new Vector2(0.5f, 0f);
            btnRt.anchoredPosition = new Vector2(0, 70);
            btnRt.sizeDelta = new Vector2(240, 60);
            Image btnImg = btnObj.AddComponent<Image>();
            btnImg.type = Image.Type.Sliced;
            btnImg.sprite = CreateRoundedRectSprite(8, 0, new Color32(50, 100, 160, 255), new Color32(0, 0, 0, 0));
            
            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            var cb = btn.colors;
            cb.normalColor = Color.white;
            cb.highlightedColor = new Color(0.8f, 0.9f, 1f);
            cb.pressedColor = new Color(0.6f, 0.8f, 1f);
            cb.selectedColor = Color.white;
            btn.colors = cb;

            GameObject btnTextObj = new GameObject("Text");
            btnTextObj.transform.SetParent(btnObj.transform, false);
            RectTransform btnTextRt = btnTextObj.AddComponent<RectTransform>();
            btnTextRt.anchorMin = Vector2.zero;
            btnTextRt.anchorMax = Vector2.one;
            btnTextRt.offsetMin = Vector2.zero;
            btnTextRt.offsetMax = Vector2.zero;
            TextMeshProUGUI btnText = Theme.UIHelper.AddText(btnTextObj, "\ud655\uc778", new Color32(255, 255, 255, 255), 28, TextAlignmentOptions.Center);
            btnText.fontStyle = FontStyles.Bold;

            btn.onClick.AddListener(() =>
            {
                if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
                Destroy(overlay);
                ShowPhotosensitivityWarning();
            });
        }
'''

if target_newgame in text and idx != -1:
    text = text.replace(target_newgame, replacement_newgame)
    text = text[:idx] + pre_alpha_method + text[idx:]
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Successfully added Pre-Alpha warning before Photosensitivity warning.")
else:
    print("Could not find targets to replace/insert.")
