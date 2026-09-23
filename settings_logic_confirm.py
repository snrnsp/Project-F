import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        private void OnDeleteDataClicked()
        {
            // Delete all save slots (0 to 9 just in case)
            for (int i = 0; i < 10; i++)
            {
                HalloweenVN.Core.SaveManager.Delete(i);
            }
            // Delete PlayerPrefs completely
            PlayerPrefs.DeleteAll();
            PlayerPrefs.Save();
            
            // Reload the current scene to reset the game completely back to the title screen
            UnityEngine.SceneManagement.SceneManager.LoadScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene().name);
        }'''

replacement = '''        private void OnDeleteDataClicked()
        {
            // Create a confirmation overlay
            GameObject overlay = new GameObject("DeleteConfirmOverlay");
            overlay.transform.SetParent(this.transform, false);
            RectTransform overlayRt = overlay.AddComponent<RectTransform>();
            overlayRt.anchorMin = Vector2.zero;
            overlayRt.anchorMax = Vector2.one;
            overlayRt.offsetMin = Vector2.zero;
            overlayRt.offsetMax = Vector2.zero;
            
            UnityEngine.UI.Image overlayImg = overlay.AddComponent<UnityEngine.UI.Image>();
            overlayImg.color = new Color(0, 0, 0, 0.85f);
            
            // Add block click
            UnityEngine.UI.Button overlayBtn = overlay.AddComponent<UnityEngine.UI.Button>();
            overlayBtn.transition = UnityEngine.UI.Selectable.Transition.None;
            
            // Panel
            GameObject panel = new GameObject("ConfirmPanel");
            panel.transform.SetParent(overlay.transform, false);
            RectTransform panelRt = panel.AddComponent<RectTransform>();
            panelRt.anchorMin = new Vector2(0.5f, 0.5f);
            panelRt.anchorMax = new Vector2(0.5f, 0.5f);
            panelRt.sizeDelta = new Vector2(500, 300);
            UnityEngine.UI.Image panelImg = panel.AddComponent<UnityEngine.UI.Image>();
            panelImg.color = new Color32(30, 20, 35, 255);
            
            // Border
            UnityEngine.UI.Outline outline = panel.AddComponent<UnityEngine.UI.Outline>();
            outline.effectColor = new Color32(200, 50, 50, 255);
            outline.effectDistance = new Vector2(2, -2);
            
            // Dummy button for panel
            UnityEngine.UI.Button panelDummyBtn = panel.AddComponent<UnityEngine.UI.Button>();
            panelDummyBtn.transition = UnityEngine.UI.Selectable.Transition.None;
            
            // Message
            GameObject msgObj = new GameObject("Message");
            msgObj.transform.SetParent(panel.transform, false);
            RectTransform msgRt = msgObj.AddComponent<RectTransform>();
            msgRt.anchorMin = new Vector2(0, 0.3f);
            msgRt.anchorMax = new Vector2(1, 1);
            msgRt.offsetMin = Vector2.zero;
            msgRt.offsetMax = Vector2.zero;
            
            UnityEngine.UI.Text msgText = msgObj.AddComponent<UnityEngine.UI.Text>();
            msgText.font = Resources.GetBuiltinResource<Font>("Arial.ttf"); // Base font, will use OS fallbacks
            msgText.text = "모든 진행 상황과 설정 데이터가 영구적으로 삭제됩니다.\\n정말 삭제하시겠습니까?";
            msgText.alignment = TextAnchor.MiddleCenter;
            msgText.fontSize = 22;
            msgText.color = Color.white;
            
            // Handle i18n
            if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.English)
                msgText.text = "All progress and settings will be permanently deleted.\\nAre you sure you want to proceed?";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.Japanese)
                msgText.text = "すべての進行状況と設定データが完全に削除されます。\\n本当に削除しますか？";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.ChineseSimplified)
                msgText.text = "所有进度和设置数据将被永久删除。\\n确定要删除吗？";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.ChineseTraditional)
                msgText.text = "所有進度和設置數據將被永久刪除。\\n確定要刪除嗎？";

            // Yes Button
            GameObject yesBtnObj = new GameObject("YesButton");
            yesBtnObj.transform.SetParent(panel.transform, false);
            RectTransform yesRt = yesBtnObj.AddComponent<RectTransform>();
            yesRt.anchorMin = new Vector2(0.5f, 0);
            yesRt.anchorMax = new Vector2(0.5f, 0);
            yesRt.anchoredPosition = new Vector2(-110, 60);
            yesRt.sizeDelta = new Vector2(160, 50);
            
            UnityEngine.UI.Image yesImg = yesBtnObj.AddComponent<UnityEngine.UI.Image>();
            yesImg.color = new Color32(180, 40, 40, 255);
            UnityEngine.UI.Button yesBtn = yesBtnObj.AddComponent<UnityEngine.UI.Button>();
            yesBtn.transition = UnityEngine.UI.Selectable.Transition.ColorTint;
            UnityEngine.UI.ColorBlock yesCb = yesBtn.colors;
            yesCb.normalColor = new Color32(180, 40, 40, 255);
            yesCb.highlightedColor = new Color32(200, 60, 60, 255);
            yesCb.pressedColor = new Color32(120, 20, 20, 255);
            yesCb.selectedColor = new Color32(180, 40, 40, 255);
            yesBtn.colors = yesCb;
            
            GameObject yesTextObj = new GameObject("Text");
            yesTextObj.transform.SetParent(yesBtnObj.transform, false);
            RectTransform yesTextRt = yesTextObj.AddComponent<RectTransform>();
            yesTextRt.anchorMin = Vector2.zero; yesTextRt.anchorMax = Vector2.one;
            yesTextRt.offsetMin = Vector2.zero; yesTextRt.offsetMax = Vector2.zero;
            UnityEngine.UI.Text yesText = yesTextObj.AddComponent<UnityEngine.UI.Text>();
            yesText.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
            yesText.text = "예";
            yesText.alignment = TextAnchor.MiddleCenter;
            yesText.fontSize = 20;
            yesText.color = Color.white;
            if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.English) yesText.text = "Yes";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.Japanese) yesText.text = "はい";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.ChineseSimplified) yesText.text = "是";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.ChineseTraditional) yesText.text = "是";

            // No Button
            GameObject noBtnObj = new GameObject("NoButton");
            noBtnObj.transform.SetParent(panel.transform, false);
            RectTransform noRt = noBtnObj.AddComponent<RectTransform>();
            noRt.anchorMin = new Vector2(0.5f, 0);
            noRt.anchorMax = new Vector2(0.5f, 0);
            noRt.anchoredPosition = new Vector2(110, 60);
            noRt.sizeDelta = new Vector2(160, 50);
            
            UnityEngine.UI.Image noImg = noBtnObj.AddComponent<UnityEngine.UI.Image>();
            noImg.color = new Color32(50, 50, 70, 255);
            UnityEngine.UI.Button noBtn = noBtnObj.AddComponent<UnityEngine.UI.Button>();
            
            GameObject noTextObj = new GameObject("Text");
            noTextObj.transform.SetParent(noBtnObj.transform, false);
            RectTransform noTextRt = noTextObj.AddComponent<RectTransform>();
            noTextRt.anchorMin = Vector2.zero; noTextRt.anchorMax = Vector2.one;
            noTextRt.offsetMin = Vector2.zero; noTextRt.offsetMax = Vector2.zero;
            UnityEngine.UI.Text noText = noTextObj.AddComponent<UnityEngine.UI.Text>();
            noText.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
            noText.text = "아니오";
            noText.alignment = TextAnchor.MiddleCenter;
            noText.fontSize = 20;
            noText.color = Color.white;
            if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.English) noText.text = "No";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.Japanese) noText.text = "いいえ";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.ChineseSimplified) noText.text = "否";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.ChineseTraditional) noText.text = "否";

            // Wire up actions
            noBtn.onClick.AddListener(() => Destroy(overlay));
            yesBtn.onClick.AddListener(() => {
                Destroy(overlay);
                ExecuteDeleteData();
            });
        }

        private void ExecuteDeleteData()
        {
            // Delete all save slots (0 to 9 just in case)
            for (int i = 0; i < 10; i++)
            {
                HalloweenVN.Core.SaveManager.Delete(i);
            }
            // Delete PlayerPrefs completely
            PlayerPrefs.DeleteAll();
            PlayerPrefs.Save();
            
            // Reload the current scene to reset the game completely back to the title screen
            UnityEngine.SceneManagement.SceneManager.LoadScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene().name);
        }'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated SettingsUI.cs logic with confirmation popup')
