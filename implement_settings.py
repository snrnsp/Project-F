import sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# STEP 1: Update SettingsData.cs — add new properties
# ============================================================
path_settings_data = 'F:/Project-F/Assets/Scripts/Core/SettingsData.cs'
with open(path_settings_data, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Add new properties
old_props = """        public static float AutoPlayDelay { get; set; } = 2.0f;
        public static int PerformanceMode { get; set; } = 1; // 0: Power Saving, 1: High Quality
        public static GameLanguage Language { get; set; } = GameLanguage.Korean;"""

new_props = """        public static float AutoPlayDelay { get; set; } = 2.0f;
        public static float DialogueBoxOpacity { get; set; } = 0.85f;
        public static bool SkipReadOnly { get; set; } = true;
        public static bool UseHandwritingFont { get; set; } = true;
        public static int PerformanceMode { get; set; } = 1; // 0: Power Saving, 1: High Quality
        public static GameLanguage Language { get; set; } = GameLanguage.Korean;"""

if old_props in content:
    content = content.replace(old_props, new_props)

# Add Load entries
old_load = """            AutoPlayDelay = PlayerPrefs.GetFloat(Prefix + "AutoPlayDelay", 2.0f);
            PerformanceMode = PlayerPrefs.GetInt(Prefix + "PerformanceMode", 1);"""

new_load = """            AutoPlayDelay = PlayerPrefs.GetFloat(Prefix + "AutoPlayDelay", 2.0f);
            DialogueBoxOpacity = PlayerPrefs.GetFloat(Prefix + "DialogueBoxOpacity", 0.85f);
            SkipReadOnly = PlayerPrefs.GetInt(Prefix + "SkipReadOnly", 1) == 1;
            UseHandwritingFont = PlayerPrefs.GetInt(Prefix + "UseHandwritingFont", 1) == 1;
            PerformanceMode = PlayerPrefs.GetInt(Prefix + "PerformanceMode", 1);"""

if old_load in content:
    content = content.replace(old_load, new_load)

# Add Save entries
old_save = """            PlayerPrefs.SetFloat(Prefix + "AutoPlayDelay", Mathf.Clamp(AutoPlayDelay, 1.0f, 5.0f));
            PlayerPrefs.SetInt(Prefix + "PerformanceMode", PerformanceMode);"""

new_save = """            PlayerPrefs.SetFloat(Prefix + "AutoPlayDelay", Mathf.Clamp(AutoPlayDelay, 1.0f, 5.0f));
            PlayerPrefs.SetFloat(Prefix + "DialogueBoxOpacity", Mathf.Clamp(DialogueBoxOpacity, 0.2f, 1.0f));
            PlayerPrefs.SetInt(Prefix + "SkipReadOnly", SkipReadOnly ? 1 : 0);
            PlayerPrefs.SetInt(Prefix + "UseHandwritingFont", UseHandwritingFont ? 1 : 0);
            PlayerPrefs.SetInt(Prefix + "PerformanceMode", PerformanceMode);"""

if old_save in content:
    content = content.replace(old_save, new_save)

# Add Reset entries
old_reset = """            AutoPlayDelay = 2.0f;
            PerformanceMode = 1;"""

new_reset = """            AutoPlayDelay = 2.0f;
            DialogueBoxOpacity = 0.85f;
            SkipReadOnly = true;
            UseHandwritingFont = true;
            PerformanceMode = 1;"""

if old_reset in content:
    content = content.replace(old_reset, new_reset)

with open(path_settings_data, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("1/3 SettingsData.cs updated")

# ============================================================
# STEP 2: Rewrite SettingsUI.cs
# ============================================================
settings_ui = r'''using UnityEngine;
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
        [SerializeField] private Text autoPlayValueText;

        // Dialogue Box Opacity
        [SerializeField] private Slider opacitySlider;
        [SerializeField] private Text opacityLabel;

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
                autoPlaySlider.minValue = 1f;
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

            UpdateAllLabels();
            UpdateLanguage();
        }

        private void OnDisable()
        {
            if (textSpeedSlider != null) textSpeedSlider.onValueChanged.RemoveListener(OnTextSpeedChanged);
            if (autoPlaySlider != null) autoPlaySlider.onValueChanged.RemoveListener(OnAutoPlayChanged);
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
            if (titleTextLabel != null) titleTextLabel.font = f;
            if (textSpeedLabel != null) textSpeedLabel.font = f;
            if (autoPlayLabel != null) autoPlayLabel.font = f;
            if (autoPlayValueText != null) autoPlayValueText.font = f;
            if (opacityLabel != null) opacityLabel.font = f;
            if (skipModeLabel != null) skipModeLabel.font = f;
            if (skipModeValueText != null) skipModeValueText.font = f;
            if (fontStyleLabel != null) fontStyleLabel.font = f;
            if (fontStyleValueText != null) fontStyleValueText.font = f;
            if (closeButtonText != null) closeButtonText.font = f;
            if (previewTextLabel != null) previewTextLabel.font = f;
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

        private void OnAutoPlayChanged(float val)
        {
            SettingsData.AutoPlayDelay = Mathf.Round(val * 10f) / 10f;
            UpdateAllLabels();
        }

        private void OnOpacityChanged(float val)
        {
            SettingsData.DialogueBoxOpacity = val;
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
        }

        private void UpdateAllLabels()
        {
            GameLanguage lang = SettingsData.Language;

            if (autoPlayValueText != null)
                autoPlayValueText.text = SettingsData.AutoPlayDelay.ToString("0.0") + "s";

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
'''

with open('F:/Project-F/Assets/Scripts/UI/SettingsUI.cs', 'w', encoding='utf-8-sig') as f:
    f.write(settings_ui)
print("2/3 SettingsUI.cs rewritten")

# ============================================================
# STEP 3: Rewrite CreateSettingsUI() in HalloweenUIBuilder.cs
# ============================================================
path_builder = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path_builder, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# Find start and end of CreateSettingsUI
start_idx = -1
end_idx = -1
brace_depth = 0
for i, line in enumerate(lines):
    if 'private void CreateSettingsUI()' in line:
        start_idx = i
    if start_idx != -1 and i >= start_idx:
        brace_depth += line.count('{') - line.count('}')
        if brace_depth == 0 and i > start_idx:
            end_idx = i + 1
            break

new_method = """        private void CreateSettingsUI()
        {
            settingsModalRoot = UIHelper.CreateUIObject("SettingsRoot", mainCanvas.transform);
            GameObject settingsRoot = settingsModalRoot;
            UIHelper.StretchFull(settingsRoot.GetComponent<RectTransform>());

            // Semi-transparent dark overlay (click to close)
            GameObject bgBtnObj = UIHelper.CreateUIObject("BackgroundButton", settingsRoot.transform);
            UIHelper.StretchFull(bgBtnObj.GetComponent<RectTransform>());
            UIHelper.AddImage(bgBtnObj, new Color(0, 0, 0, 0.7f));
            UnityEngine.UI.Button bgBtn = bgBtnObj.AddComponent<UnityEngine.UI.Button>();
            bgBtn.transition = UnityEngine.UI.Selectable.Transition.None;

            // Settings panel (taller to fit new options)
            GameObject panel = UIHelper.CreatePanel("SettingsPanel", settingsRoot.transform, HalloweenTheme.PanelBackground);
            UnityEngine.UI.Outline outline = panel.GetComponent<UnityEngine.UI.Outline>();
            if (outline != null) outline.effectDistance = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth + 4f);
            RectTransform panelRt = panel.GetComponent<RectTransform>();
            UIHelper.SetAnchors(panelRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            panelRt.sizeDelta = new Vector2(700, 750);

            // Title
            GameObject titleObj = UIHelper.CreateUIObject("Title", panel.transform);
            RectTransform titleRt = titleObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            titleRt.anchoredPosition = new Vector2(0, -30);
            titleRt.sizeDelta = new Vector2(400, 55);
            Text titleText = CreateLegacyText(titleObj, "\\uC124\\uC815", HalloweenTheme.AccentOrange, 42, TextAnchor.UpperCenter);

            float yPos = -75;

            // ─── 1. Text Speed ───
            var textSpeedLabel = CreateSettingsLabel(panel.transform, "\\uD14D\\uC2A4\\uD2B8 \\uC18D\\uB3C4", yPos);
            Slider textSpeedSlider = CreateSettingsSlider(panel.transform, yPos - 30);

            // Preview Text
            yPos -= 65;
            GameObject previewObj = UIHelper.CreateUIObject("PreviewText", panel.transform);
            RectTransform previewRt = previewObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(previewRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            previewRt.anchoredPosition = new Vector2(0, yPos);
            previewRt.sizeDelta = new Vector2(600, 40);
            Text previewText = CreateLegacyText(previewObj, "", HalloweenTheme.TextPrimary, 24, TextAnchor.MiddleCenter);

            // ─── 2. Auto-play Delay ───
            yPos -= 60;
            var autoPlayLabel = CreateSettingsLabel(panel.transform, "\\uC624\\uD1A0 \\uB300\\uAE30 \\uC2DC\\uAC04", yPos);
            // Value text (right-aligned)
            GameObject autoValObj = UIHelper.CreateUIObject("AutoPlayValue", panel.transform);
            RectTransform autoValRt = autoValObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(autoValRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            autoValRt.anchoredPosition = new Vector2(200, yPos);
            autoValRt.sizeDelta = new Vector2(100, 35);
            Text autoPlayValueText = CreateLegacyText(autoValObj, "2.0s", HalloweenTheme.AccentOrange, 26, TextAnchor.UpperRight);
            Slider autoPlaySlider = CreateSettingsSlider(panel.transform, yPos - 30);

            // ─── 3. Dialogue Box Opacity ───
            yPos -= 70;
            var opacityLabel = CreateSettingsLabel(panel.transform, "\\uB300\\uC0AC\\uCC3D \\uD22C\\uBA85\\uB3C4", yPos);
            Slider opacitySlider = CreateSettingsSlider(panel.transform, yPos - 30);

            // ─── 4. Skip Mode (toggle button) ───
            yPos -= 70;
            var skipModeLabel = CreateSettingsLabel(panel.transform, "\\uC2A4\\uD0B5 \\uBAA8\\uB4DC", yPos);
            var skipTuple = CreateLegacyButton(panel.transform, "\\uC77D\\uC740 \\uB300\\uC0AC\\uB9CC", 220, 40, new Color32(60, 40, 80, 255));
            RectTransform skipRt = skipTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(skipRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            skipRt.anchoredPosition = new Vector2(90, yPos - 5);
            skipTuple.text.fontSize = 22;

            // ─── 5. Font Style (toggle button) ───
            yPos -= 55;
            var fontStyleLabel = CreateSettingsLabel(panel.transform, "\\uAE00\\uAF34", yPos);
            var fontTuple = CreateLegacyButton(panel.transform, "\\uC190\\uAE00\\uC528", 220, 40, new Color32(60, 40, 80, 255));
            RectTransform fontRt = fontTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(fontRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            fontRt.anchoredPosition = new Vector2(90, yPos - 5);
            fontTuple.text.fontSize = 22;

            // ─── Close Button ───
            var closeTuple = CreateLegacyButton(panel.transform, "\\uB2EB\\uAE30", 200, 50, HalloweenTheme.ButtonNormal);
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(0, 40);
            closeTuple.text.fontSize = 28;

            // Attach SettingsUI
            SettingsUI settingsUi = settingsRoot.AddComponent<SettingsUI>();
            settingsUiRef = settingsUi;
            bgBtn.onClick.AddListener(() => settingsUi.Hide());
            if (globalMgrRef != null) globalMgrRef.Initialize(settingsRoot);
            UIHelper.SetField(settingsUi, "settingsPanel", settingsRoot);
            UIHelper.SetField(settingsUi, "titleTextLabel", titleText);
            UIHelper.SetField(settingsUi, "textSpeedSlider", textSpeedSlider);
            UIHelper.SetField(settingsUi, "textSpeedLabel", textSpeedLabel);
            UIHelper.SetField(settingsUi, "previewTextLabel", previewText);
            UIHelper.SetField(settingsUi, "autoPlaySlider", autoPlaySlider);
            UIHelper.SetField(settingsUi, "autoPlayLabel", autoPlayLabel);
            UIHelper.SetField(settingsUi, "autoPlayValueText", autoPlayValueText);
            UIHelper.SetField(settingsUi, "opacitySlider", opacitySlider);
            UIHelper.SetField(settingsUi, "opacityLabel", opacityLabel);
            UIHelper.SetField(settingsUi, "skipModeButton", skipTuple.btn);
            UIHelper.SetField(settingsUi, "skipModeLabel", skipModeLabel);
            UIHelper.SetField(settingsUi, "skipModeValueText", skipTuple.text);
            UIHelper.SetField(settingsUi, "fontStyleButton", fontTuple.btn);
            UIHelper.SetField(settingsUi, "fontStyleLabel", fontStyleLabel);
            UIHelper.SetField(settingsUi, "fontStyleValueText", fontTuple.text);
            UIHelper.SetField(settingsUi, "closeButtonText", closeTuple.text);
            UIHelper.SetField(settingsUi, "closeButton", closeTuple.btn);

            settingsRoot.SetActive(false);

            // Wire lobby settings button
            if (settingsButtonRef != null)
            {
                settingsButtonRef.onClick.AddListener(() => settingsUi.Show());
            }
        }
"""

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + [new_method] + lines[end_idx:]
    with open(path_builder, 'w', encoding='utf-8-sig') as fw:
        fw.writelines(lines)
    print("3/3 HalloweenUIBuilder.cs CreateSettingsUI rewritten")
else:
    print("ERROR: Could not find CreateSettingsUI boundaries")

# ============================================================
# STEP 4: Add ApplyOpacity stub to DialogueUI.cs
# ============================================================
path_dialogue = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path_dialogue, 'r', encoding='utf-8-sig') as f:
    content = f.read()

if 'public void ApplyOpacity' not in content:
    # Find the class closing and insert before it
    old_end = """        private float SpeedToSlider(float speed)"""
    stub = """        public void ApplyOpacity(float opacity)
        {
            if (dialoguePanel != null)
            {
                var img = dialoguePanel.GetComponent<UnityEngine.UI.Image>();
                if (img != null)
                {
                    Color c = img.color;
                    c.a = opacity;
                    img.color = c;
                }
            }
        }

        private float SpeedToSlider(float speed)"""
    
    if old_end in content:
        content = content.replace(old_end, stub)
        with open(path_dialogue, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        print("4/4 DialogueUI.cs ApplyOpacity added")
    else:
        # Try alternative: just append before final }}
        print("4/4 SKIP - SpeedToSlider not found, ApplyOpacity may need manual addition")
else:
    print("4/4 SKIP - ApplyOpacity already exists")

# ============================================================
# STEP 5: Update FontHelper to respect UseHandwritingFont
# ============================================================
path_fonthelper = 'F:/Project-F/Assets/Scripts/UI/FontHelper.cs'
with open(path_fonthelper, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_getfontname = """        public static string GetFontNameForLanguage(GameLanguage lang) {
            switch (lang) {
                case GameLanguage.English: return "Caveat-Regular";
                case GameLanguage.Japanese: return "ZenKurenaido-Regular";
                case GameLanguage.ChineseSimplified: return "MaShanZheng-Regular";
                case GameLanguage.ChineseTraditional: return "ZenKurenaido-Regular"; // NanumPenScript has huge Hanja (Traditional) coverage!
                default: return "NanumPenScript";
            }
        }"""

new_getfontname = """        public static string GetFontNameForLanguage(GameLanguage lang) {
            if (!SettingsData.UseHandwritingFont) return "MalgunGothic";
            switch (lang) {
                case GameLanguage.English: return "Caveat-Regular";
                case GameLanguage.Japanese: return "ZenKurenaido-Regular";
                case GameLanguage.ChineseSimplified: return "MaShanZheng-Regular";
                case GameLanguage.ChineseTraditional: return "ZenKurenaido-Regular";
                default: return "NanumPenScript";
            }
        }"""

if old_getfontname in content:
    content = content.replace(old_getfontname, new_getfontname)
    with open(path_fonthelper, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("5/5 FontHelper.cs updated with UseHandwritingFont check")
else:
    print("5/5 SKIP - FontHelper pattern not found")
