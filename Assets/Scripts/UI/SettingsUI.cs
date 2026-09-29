using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using HalloweenVN.Core;

namespace HalloweenVN.UI
{
    public class SettingsUI : MonoBehaviour
    {
        [SerializeField] private GameObject settingsPanel;

        // Text Speed
        [SerializeField] private Slider textSpeedSlider;
        [SerializeField] private Text textSpeedLabel;
        [SerializeField] private Text previewTextLabel;

        // Auto-play Delay
        [SerializeField] private Slider autoPlaySlider;
        [SerializeField] private Text autoPlayLabel;
        [SerializeField] private InputField autoPlayInputField;

        // Dialogue Box Opacity
        [SerializeField] private Slider opacitySlider;
        [SerializeField] private Text opacityLabel;
        [SerializeField] private Image previewBoxImage;

        // Skip Mode Toggle
        [SerializeField] private Button skipModeButton;
        [SerializeField] private Text skipModeLabel;
        [SerializeField] private Text skipModeValueText;

        // Font Style Toggle
        [SerializeField] private Button fontStyleButton;
        [SerializeField] private Text fontStyleLabel;
        [SerializeField] private Text fontStyleValueText;

        // Title / Close
        [SerializeField] private Text titleTextLabel;
        [SerializeField] private Text closeButtonText;
        [SerializeField] private Button closeButton;

        // Legacy compat (unused but kept for SetField safety)
        [SerializeField] private Slider bgmVolumeSlider;
        [SerializeField] private Text bgmVolumeLabel;
        [SerializeField] private Slider sfxVolumeSlider;
        [SerializeField] private Text sfxVolumeLabel;
        [SerializeField] private Toggle fullscreenToggle;

        private Coroutine typingCoroutine;
        private string previewMessage = "\uD14D\uC2A4\uD2B8 \uC18D\uB3C4\uAC00 \uC774 \uC815\uB3C4\uB85C \uCD9C\uB825\uB429\uB2C8\uB2E4. \uB208\uC73C\uB85C \uD655\uC778\uD574 \uBCF4\uC138\uC694!";

        private static System.Collections.Generic.Dictionary<string, Font> _legacyFontCache = new System.Collections.Generic.Dictionary<string, Font>();
        private Font GetLegacyFont(string name) {
            if (string.IsNullOrEmpty(name)) return null;
            if (_legacyFontCache.ContainsKey(name)) return _legacyFontCache[name];
            Font rawFont = Resources.Load<Font>("Fonts/" + name);
            if (rawFont != null) _legacyFontCache[name] = rawFont;
            return rawFont;
        }

        private void OnEnable()
        {
            if (textSpeedSlider != null)
            {
                textSpeedSlider.value = SpeedToSlider(SettingsData.TextSpeed);
                textSpeedSlider.onValueChanged.AddListener(OnTextSpeedChanged);
            }
            if (autoPlaySlider != null)
            {
                autoPlaySlider.minValue = 0.1f;
                autoPlaySlider.maxValue = 5f;
                autoPlaySlider.value = SettingsData.AutoPlayDelay;
                autoPlaySlider.onValueChanged.AddListener(OnAutoPlayChanged);
            }
            if (opacitySlider != null)
            {
                opacitySlider.minValue = 0.2f;
                opacitySlider.maxValue = 1f;
                opacitySlider.value = SettingsData.DialogueBoxOpacity;
                opacitySlider.onValueChanged.AddListener(OnOpacityChanged);
            }
            if (skipModeButton != null)
            {
                skipModeButton.onClick.AddListener(OnSkipModeToggled);
            }
            if (fontStyleButton != null)
            {
                fontStyleButton.onClick.AddListener(OnFontStyleToggled);
            }
            if (closeButton != null)
            {
                closeButton.onClick.AddListener(Hide);
            }

            if (autoPlayInputField != null) autoPlayInputField.onEndEdit.AddListener(OnAutoPlayInputEdit);
        UpdateAllLabels();
            UpdateLanguage();
        }

        private void OnDisable()
        {
            if (textSpeedSlider != null) textSpeedSlider.onValueChanged.RemoveListener(OnTextSpeedChanged);
            if (autoPlaySlider != null) autoPlaySlider.onValueChanged.RemoveListener(OnAutoPlayChanged);
        if (autoPlayInputField != null) autoPlayInputField.onEndEdit.RemoveListener(OnAutoPlayInputEdit);
            if (opacitySlider != null) opacitySlider.onValueChanged.RemoveListener(OnOpacityChanged);
            if (skipModeButton != null) skipModeButton.onClick.RemoveListener(OnSkipModeToggled);
            if (fontStyleButton != null) fontStyleButton.onClick.RemoveListener(OnFontStyleToggled);
            if (closeButton != null) closeButton.onClick.RemoveListener(Hide);
        }

        public void UpdateLanguage()
        {
            GameLanguage lang = SettingsData.Language;
            string fontName = FontHelper.GetFontNameForLanguage(lang);
            Font f = GetLegacyFont(fontName);
            if (f != null)
            {
                ApplyFontToAll(f);
            }

            switch (lang)
            {
                case GameLanguage.Korean:
                    SetText(titleTextLabel, "\uC124\uC815");
                    SetText(textSpeedLabel, "\uD14D\uC2A4\uD2B8 \uC18D\uB3C4");
                    SetText(autoPlayLabel, "\uC624\uD1A0 \uB300\uAE30 \uC2DC\uAC04");
                    SetText(opacityLabel, "\uB300\uC0AC\uCC3D \uD22C\uBA85\uB3C4");
                    SetText(skipModeLabel, "\uC2A4\uD0B5 \uBAA8\uB4DC");
                    SetText(fontStyleLabel, "\uAE00\uAF34");
                    SetText(closeButtonText, "\uB2EB\uAE30");
                    previewMessage = "\uD14D\uC2A4\uD2B8 \uC18D\uB3C4\uAC00 \uC774 \uC815\uB3C4\uB85C \uCD9C\uB825\uB429\uB2C8\uB2E4. \uB208\uC73C\uB85C \uD655\uC778\uD574 \uBCF4\uC138\uC694!";
                    break;
                case GameLanguage.English:
                    SetText(titleTextLabel, "Settings");
                    SetText(textSpeedLabel, "Text Speed");
                    SetText(autoPlayLabel, "Auto-play Delay");
                    SetText(opacityLabel, "Box Opacity");
                    SetText(skipModeLabel, "Skip Mode");
                    SetText(fontStyleLabel, "Font");
                    SetText(closeButtonText, "Close");
                    previewMessage = "This is a text speed test. Please check it carefully!";
                    break;
                case GameLanguage.Japanese:
                    SetText(titleTextLabel, "\u8A2D\u5B9A");
                    SetText(textSpeedLabel, "\u30C6\u30AD\u30B9\u30C8\u901F\u5EA6");
                    SetText(autoPlayLabel, "\u30AA\u30FC\u30C8\u5F85\u6A5F\u6642\u9593");
                    SetText(opacityLabel, "\u30C0\u30A4\u30A2\u30ED\u30B0\u900F\u660E\u5EA6");
                    SetText(skipModeLabel, "\u30B9\u30AD\u30C3\u30D7\u30E2\u30FC\u30C9");
                    SetText(fontStyleLabel, "\u30D5\u30A9\u30F3\u30C8");
                    SetText(closeButtonText, "\u9589\u3058\u308B");
                    previewMessage = "\u30C6\u30AD\u30B9\u30C8\u901F\u5EA6\u306E\u30C6\u30B9\u30C8\u3067\u3059\u3002\u3054\u78BA\u8A8D\u304F\u3060\u3055\u3044\u3002";
                    break;
                case GameLanguage.ChineseSimplified:
                    SetText(titleTextLabel, "\u8BBE\u7F6E");
                    SetText(textSpeedLabel, "\u6587\u672C\u901F\u5EA6");
                    SetText(autoPlayLabel, "\u81EA\u52A8\u64AD\u653E\u5EF6\u8FDF");
                    SetText(opacityLabel, "\u5BF9\u8BDD\u6846\u900F\u660E\u5EA6");
                    SetText(skipModeLabel, "\u8DF3\u8FC7\u6A21\u5F0F");
                    SetText(fontStyleLabel, "\u5B57\u4F53");
                    SetText(closeButtonText, "\u5173\u95ED");
                    previewMessage = "\u8FD9\u662F\u6587\u672C\u901F\u5EA6\u6D4B\u8BD5\u3002\u8BF7\u4ED4\u7EC6\u68C0\u67E5\uFF01";
                    break;
                case GameLanguage.ChineseTraditional:
                    SetText(titleTextLabel, "\u8A2D\u5B9A");
                    SetText(textSpeedLabel, "\u6587\u672C\u901F\u5EA6");
                    SetText(autoPlayLabel, "\u81EA\u52D5\u64AD\u653E\u5EF6\u9072");
                    SetText(opacityLabel, "\u5C0D\u8A71\u6846\u900F\u660E\u5EA6");
                    SetText(skipModeLabel, "\u8DF3\u904E\u6A21\u5F0F");
                    SetText(fontStyleLabel, "\u5B57\u9AD4");
                    SetText(closeButtonText, "\u95DC\u9589");
                    previewMessage = "\u9019\u662F\u6587\u672C\u901F\u5EA6\u6E2C\u8A66\u3002\u8ACB\u4ED4\u7D30\u6AA2\u67E5\u3002";
                    break;
            }

            UpdateAllLabels();
            PlayPreviewText();
        }

        private void SetText(Text t, string s) { if (t != null) t.text = s; }

        private void ApplyFontToAll(Font f)
        {
            bool isGothic = !SettingsData.UseHandwritingFont;
            
            void SetFont(Text t, int defaultSize, int gothicSize)
            {
                if (t != null) {
                    t.font = f;
                    t.fontSize = isGothic ? gothicSize : defaultSize;
                }
            }

            SetFont(titleTextLabel, 42, 32);
            SetFont(textSpeedLabel, 28, 22);
            SetFont(autoPlayLabel, 28, 22);
            SetFont(opacityLabel, 28, 22);
            SetFont(skipModeLabel, 28, 22);
            SetFont(fontStyleLabel, 28, 22);
            
            SetFont(skipModeValueText, 20, 16);
            SetFont(fontStyleValueText, 20, 16);
            SetFont(closeButtonText, 28, 22);
            SetFont(previewTextLabel, 24, 20);

            if (autoPlayInputField != null) {
                autoPlayInputField.text = SettingsData.AutoPlayDelay.ToString("0.0");
                if (autoPlayInputField.textComponent != null) {
                    autoPlayInputField.textComponent.font = f;
                    autoPlayInputField.textComponent.fontSize = isGothic ? 16 : 20;
                }
            }
        }

        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
            if (settingsPanel != null)
            {
                settingsPanel.SetActive(true);
                if (textSpeedSlider != null) textSpeedSlider.value = SpeedToSlider(SettingsData.TextSpeed);
                if (autoPlaySlider != null) autoPlaySlider.value = SettingsData.AutoPlayDelay;
                if (opacitySlider != null) opacitySlider.value = SettingsData.DialogueBoxOpacity;
                if (previewBoxImage != null)
                {
                    Color c = previewBoxImage.color;
                    c.a = SettingsData.DialogueBoxOpacity;
                    previewBoxImage.color = c;
                }
                UpdateAllLabels();
                PlayPreviewText();
            }
        }

        public void Hide()
        {
            SettingsData.Save();
            if (settingsPanel != null) settingsPanel.SetActive(false);
            if (typingCoroutine != null)
            {
                StopCoroutine(typingCoroutine);
                typingCoroutine = null;
            }
        }

        // --- Callbacks ---

        private void OnTextSpeedChanged(float val)
        {
            SettingsData.TextSpeed = SliderToSpeed(val);
        }

        
    private void OnAutoPlayInputEdit(string val)
    {
        if (float.TryParse(val, out float result))
        {
            result = Mathf.Clamp(result, 0.1f, 5.0f);
            if (autoPlaySlider != null)
            {
                autoPlaySlider.value = result;
            }
            else
            {
                SettingsData.AutoPlayDelay = result;
                SettingsData.Save();
            }
            autoPlayInputField.text = result.ToString("0.0");
        }
        else
        {
            autoPlayInputField.text = SettingsData.AutoPlayDelay.ToString("0.0");
        }
    }

    private void OnAutoPlayChanged(float val)
        {
            SettingsData.AutoPlayDelay = Mathf.Round(val * 10f) / 10f;
            UpdateAllLabels();
        }

        private void OnOpacityChanged(float val)
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
        }

        private void OnSkipModeToggled()
        {
            SettingsData.SkipReadOnly = !SettingsData.SkipReadOnly;
            UpdateAllLabels();
        }

        private void OnFontStyleToggled()
        {
            SettingsData.UseHandwritingFont = !SettingsData.UseHandwritingFont;
            SettingsData.Save();
            UpdateAllLabels();

            // Trigger global font refresh
            var langUi = Object.FindAnyObjectByType<LanguageUI>(FindObjectsInactive.Include);
            // Re-apply fonts by triggering UpdateLanguage on all UIs
            var lobby = Object.FindAnyObjectByType<LobbyUI>();
            if (lobby != null) lobby.UpdateLanguage();
            UpdateLanguage();
            var dialogue = Object.FindAnyObjectByType<DialogueUI>(FindObjectsInactive.Include);
            if (dialogue != null) dialogue.UpdateLanguage();
            var extra = Object.FindAnyObjectByType<ExtraUI>(FindObjectsInactive.Include);
            if (extra != null) extra.UpdateLanguage();
        }

        private void UpdateAllLabels()
        {
            GameLanguage lang = SettingsData.Language;

            if (autoPlayInputField != null) autoPlayInputField.text = SettingsData.AutoPlayDelay.ToString("0.0");
            if (skipModeValueText != null)
            {
                switch (lang)
                {
                    case GameLanguage.Korean:
                        skipModeValueText.text = SettingsData.SkipReadOnly ? "\uC77D\uC740 \uB300\uC0AC\uB9CC" : "\uBAA8\uB4E0 \uB300\uC0AC";
                        break;
                    case GameLanguage.English:
                        skipModeValueText.text = SettingsData.SkipReadOnly ? "Read Only" : "All Text";
                        break;
                    case GameLanguage.Japanese:
                        skipModeValueText.text = SettingsData.SkipReadOnly ? "\u65E2\u8AAD\u306E\u307F" : "\u5168\u3066";
                        break;
                    case GameLanguage.ChineseSimplified:
                        skipModeValueText.text = SettingsData.SkipReadOnly ? "\u5DF2\u8BFB" : "\u5168\u90E8";
                        break;
                    default:
                        skipModeValueText.text = SettingsData.SkipReadOnly ? "\u5DF2\u8B80" : "\u5168\u90E8";
                        break;
                }
            }

            if (fontStyleValueText != null)
            {
                switch (lang)
                {
                    case GameLanguage.Korean:
                        fontStyleValueText.text = SettingsData.UseHandwritingFont ? "\uC190\uAE00\uC528" : "\uACE0\uB515";
                        break;
                    case GameLanguage.English:
                        fontStyleValueText.text = SettingsData.UseHandwritingFont ? "Handwriting" : "Gothic";
                        break;
                    case GameLanguage.Japanese:
                        fontStyleValueText.text = SettingsData.UseHandwritingFont ? "\u624B\u66F8\u304D" : "\u30B4\u30B7\u30C3\u30AF";
                        break;
                    case GameLanguage.ChineseSimplified:
                        fontStyleValueText.text = SettingsData.UseHandwritingFont ? "\u624B\u5199" : "\u9ED1\u4F53";
                        break;
                    default:
                        fontStyleValueText.text = SettingsData.UseHandwritingFont ? "\u624B\u5BEB" : "\u9ED1\u9AD4";
                        break;
                }
            }
        }

        // --- Preview ---

        private void PlayPreviewText()
        {
            if (previewTextLabel == null) return;
            if (typingCoroutine != null) StopCoroutine(typingCoroutine);
            if (gameObject.activeInHierarchy)
                typingCoroutine = StartCoroutine(TypePreviewCoroutine());
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

        // --- Conversion ---

        private float SpeedToSlider(float speed)
        {
            float t = Mathf.InverseLerp(0.05f, 0.005f, speed);
            return Mathf.Lerp(0f, 1f, t);
        }

        private float SliderToSpeed(float sliderVal)
        {
            float t = Mathf.InverseLerp(0f, 1f, sliderVal);
            return Mathf.Lerp(0.05f, 0.005f, t);
        }
    }
}
