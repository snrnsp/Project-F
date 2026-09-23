﻿﻿﻿﻿﻿﻿using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using HalloweenVN.Core;

namespace HalloweenVN.UI
{
    public class SettingsUI : MonoBehaviour
    {
        [SerializeField] private GameObject settingsPanel;
        [SerializeField] private Slider textSpeedSlider;
        [SerializeField] private Text textSpeedLabel;
        [SerializeField] private Slider bgmVolumeSlider;
        [SerializeField] private Text bgmVolumeLabel;
        [SerializeField] private Slider sfxVolumeSlider;
        [SerializeField] private Text sfxVolumeLabel;
        [SerializeField] private Toggle fullscreenToggle;
        [SerializeField] private Button closeButton;
        [SerializeField] private Button deleteDataButton;
        
        [SerializeField] private Text previewTextLabel;
        [SerializeField] private Text titleTextLabel;
        [SerializeField] private Text closeButtonText;
        [SerializeField] private Text deleteDataButtonText;
        private Coroutine typingCoroutine;
        private string previewMessage = "\uD14D\uC2A4\uD2B8 \uC18D\uB3C4\uAC00 \uC774 \uC815\uB3C4\uB85C \uCD9C\uB825\uB429\uB2C8\uB2E4. \uB208\uC73C\uB85C \uD655\uC778\uD574 \uBCF4\uC138\uC694!";

        private void OnEnable()
        {
            if (textSpeedSlider != null)
            {
                textSpeedSlider.value = SpeedToSlider(SettingsData.TextSpeed);
                textSpeedSlider.onValueChanged.AddListener(OnTextSpeedChanged);
            }
            if (bgmVolumeSlider != null)
            {
                bgmVolumeSlider.value = SettingsData.BGMVolume;
                bgmVolumeSlider.onValueChanged.AddListener(OnBGMVolumeChanged);
            }
            if (sfxVolumeSlider != null)
            {
                sfxVolumeSlider.value = SettingsData.SFXVolume;
                sfxVolumeSlider.onValueChanged.AddListener(OnSFXVolumeChanged);
            }
            if (fullscreenToggle != null)
            {
                fullscreenToggle.isOn = SettingsData.IsFullScreen;
                fullscreenToggle.onValueChanged.AddListener(OnFullscreenChanged);
            }
            if (closeButton != null)
            {
                closeButton.onClick.AddListener(Hide);
            }
            if (deleteDataButton != null)
            {
                deleteDataButton.onClick.AddListener(OnDeleteDataClicked);
            }

            UpdateLabels();
            UpdateLanguage();
        }

        public void UpdateLanguage()
        {
            GameLanguage lang = SettingsData.Language;

            if (lang == GameLanguage.Korean)
            {
                if (titleTextLabel != null) titleTextLabel.text = "\uC124\uC815";
                if (textSpeedLabel != null) textSpeedLabel.text = "\uD14D\uC2A4\uD2B8 \uC18D\uB3C4";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "BGM";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "SFX";
                if (closeButtonText != null) closeButtonText.text = "\uB2EB\uAE30";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "데이터 삭제";
                previewMessage = "\uD14D\uC2A4\uD2B8 \uC18D\uB3C4\uAC00 \uC774 \uC815\uB3C4\uB85C \uCD9C\uB825\uB429\uB2C8\uB2E4. \uB208\uC73C\uB85C \uD655\uC778\uD574 \uBCF4\uC138\uC694!";
            }
            else if (lang == GameLanguage.English)
            {
                if (titleTextLabel != null) titleTextLabel.text = "Settings";
                if (textSpeedLabel != null) textSpeedLabel.text = "Text Speed";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "BGM";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "SFX";
                if (closeButtonText != null) closeButtonText.text = "Close";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "Delete Data";
                previewMessage = "This is a text speed test. Please check it carefully!";
            }
            else if (lang == GameLanguage.Japanese)
            {
                if (titleTextLabel != null) titleTextLabel.text = "\u8A2D\u5B9A";
                if (textSpeedLabel != null) textSpeedLabel.text = "\u30C6\u30AD\u30B9\u30C8\u901F\u5EA6";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "BGM";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "SFX";
                if (closeButtonText != null) closeButtonText.text = "\u9589\u3058\u308B";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "データ削除";
                previewMessage = "\u30C6\u30AD\u30B9\u30C8\u901F\u5EA6\u306E\u30C6\u30B9\u30C8\u3067\u3059\u3002\u3054\u78BA\u8A8D\u304F\u3060\u3055\u3044\u3002";
            }
            else if (lang == GameLanguage.ChineseSimplified)
            {
                if (titleTextLabel != null) titleTextLabel.text = "\u8BBE\u7F6E";
                if (textSpeedLabel != null) textSpeedLabel.text = "\u6587\u672C\u901F\u5EA6";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "\u80CC\u666F\u97F3\u4E50";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "\u97F3\u6548";
                if (closeButtonText != null) closeButtonText.text = "\u5173\u95ED";
                if (deleteDataButtonText != null) deleteDataButtonText.text = "删除数据";
                previewMessage = "\u8FD9\u662F\u6587\u672C\u901F\u5EA6\u6D4B\u8BD5\u3002\u8BF7\u4ED4\u7EC6\u68C0\u67E5\uFF01";
            }
            else if (lang == GameLanguage.ChineseTraditional)
            {
                if (titleTextLabel != null) titleTextLabel.text = "\u8A2D\u5B9A";
                if (textSpeedLabel != null) textSpeedLabel.text = "\u6587\u672C\u901F\u5EA6";
                if (bgmVolumeLabel != null) bgmVolumeLabel.text = "\u80CC\u666F\u97F3\u6A02";
                if (sfxVolumeLabel != null) sfxVolumeLabel.text = "\u97F3\u6548";
                if (closeButtonText != null) closeButtonText.text = "\u95DC\u9589";
                previewMessage = "\u9019\u662F\u6587\u672C\u901F\u5EA6\u6E2C\u8A66\u3002\u8ACB\u4ED4\u7D30\u6AA2\u67E5\u3002";
            }
            
            PlayPreviewText();
        }

        private void OnDisable()
        {
            if (textSpeedSlider != null) textSpeedSlider.onValueChanged.RemoveListener(OnTextSpeedChanged);
            if (bgmVolumeSlider != null) bgmVolumeSlider.onValueChanged.RemoveListener(OnBGMVolumeChanged);
            if (sfxVolumeSlider != null) sfxVolumeSlider.onValueChanged.RemoveListener(OnSFXVolumeChanged);
            if (fullscreenToggle != null) fullscreenToggle.onValueChanged.RemoveListener(OnFullscreenChanged);
            if (closeButton != null) closeButton.onClick.RemoveListener(Hide);
        }

        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(true);
                if (textSpeedSlider != null) textSpeedSlider.value = SpeedToSlider(SettingsData.TextSpeed);
                if (bgmVolumeSlider != null) bgmVolumeSlider.value = SettingsData.BGMVolume;
                if (sfxVolumeSlider != null) sfxVolumeSlider.value = SettingsData.SFXVolume;
                if (fullscreenToggle != null) fullscreenToggle.isOn = SettingsData.IsFullScreen;
                
                UpdateLabels();
                PlayPreviewText();
            }
        }

        private void OnDeleteDataClicked()
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
            
            string[] fontNames = { 
                "Malgun Gothic", "Apple SD Gothic Neo",
                "Meiryo", "Yu Gothic", "MS Gothic", "Hiragino Sans",
                "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC",
                "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC",
                "Arial Unicode MS", "sans-serif"
            };
            Font cjkFont = Font.CreateDynamicFontFromOSFont(fontNames, 22);
            if (cjkFont == null) cjkFont = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            msgText.font = cjkFont;

            msgText.text = "모든 진행 상황과 설정 데이터가 영구적으로 삭제됩니다.\n정말 삭제하시겠습니까?";
            msgText.alignment = TextAnchor.MiddleCenter;
            msgText.fontSize = 22;
            msgText.color = Color.white;
            
            // Handle i18n
            if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.English)
                msgText.text = "All progress and settings will be permanently deleted.\nAre you sure you want to proceed?";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.Japanese)
                msgText.text = "すべての進行状況と設定データが完全に削除されます。\n本当に削除しますか？";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.ChineseSimplified)
                msgText.text = "所有进度和设置数据将被永久删除。\n确定要删除吗？";
            else if (HalloweenVN.Core.SettingsData.Language == HalloweenVN.Core.GameLanguage.ChineseTraditional)
                msgText.text = "所有進度和設置數據將被永久刪除。\n確定要刪除嗎？";

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
            yesText.font = cjkFont;
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
            noText.font = cjkFont;
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
        }

        public void Hide()
        {
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(false);
            }
            if (typingCoroutine != null)
            {
                StopCoroutine(typingCoroutine);
                typingCoroutine = null;
            }
        }

        private void PlayPreviewText()
        {
            if (previewTextLabel == null) return;
            
            if (typingCoroutine != null)
            {
                StopCoroutine(typingCoroutine);
            }
            
            if (gameObject.activeInHierarchy)
            {
                typingCoroutine = StartCoroutine(TypePreviewCoroutine());
            }
        }
        
        private System.Collections.IEnumerator TypePreviewCoroutine()
        {
            int totalChars = previewMessage.Length;
            
            while (true)
            {
                previewTextLabel.text = "";
                
                for (int i = 0; i <= totalChars; i++)
                {
                    previewTextLabel.text = previewMessage.Substring(0, i);
                    yield return new WaitForSeconds(SettingsData.TextSpeed);
                }
                
                yield return new WaitForSeconds(0.5f);
            }
        }

        private void OnTextSpeedChanged(float val)
        {
            SettingsData.TextSpeed = SliderToSpeed(val);
            UpdateLabels();
            PlayPreviewText();
        }

        private void OnBGMVolumeChanged(float val)
        {
            SettingsData.BGMVolume = val;
            UpdateLabels();
        }

        private void OnSFXVolumeChanged(float val)
        {
            SettingsData.SFXVolume = val;
            UpdateLabels();
        }

        private void OnFullscreenChanged(bool val)
        {
            SettingsData.IsFullScreen = val;
            Screen.fullScreen = val;
        }

        private void UpdateLabels()
        {
        }

        private float SpeedToSlider(float speed)
        {
            float t = Mathf.InverseLerp(0.1f, 0.01f, speed);
            return Mathf.Lerp(0f, 100f, t);
        }

        private float SliderToSpeed(float sliderVal)
        {
            float t = Mathf.InverseLerp(0f, 100f, sliderVal);
            return Mathf.Lerp(0.1f, 0.01f, t);
        }
    }
}