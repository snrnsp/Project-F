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
                // Skip Mode Toggle
        [SerializeField] private Button ctrlSkipButton;

        [SerializeField] private Text skipModeLabel;
        [SerializeField] private Button skipHelpButton;
        [SerializeField] private GameObject skipHelpPanel;
        [SerializeField] private Text skipHelpText;
        [SerializeField] private Text ctrlSkipValueText;
        [SerializeField] private GameObject skipDropdownPanel;
        [SerializeField] private Button skipOptCtrl;
        [SerializeField] private Button skipOptShift;
        [SerializeField] private Button skipOptSpace;

        // Font Style Toggle
        [SerializeField] private Button fontStyleButton;
        [SerializeField] private Text fontStyleLabel;
        [SerializeField] private Text fontStyleValueText;

        // Title / Close
        [SerializeField] private Text titleTextLabel;
        [SerializeField] private Button closeButton;
        [SerializeField] private Button returnToTitleButton;
        [SerializeField] private Text returnToTitleLabel;

        // Legacy compat (unused but kept for SetField safety)
        [SerializeField] private Slider bgmVolumeSlider;
        [SerializeField] private Text bgmVolumeLabel;
        [SerializeField] private Slider sfxVolumeSlider;
        [SerializeField] private Text sfxVolumeLabel;
        [SerializeField] private Text bgmVolumeValueText;
        [SerializeField] private Text sfxVolumeValueText;
        private float lastSfxPreviewTime = -1f;
        [SerializeField] private Toggle fullscreenToggle;

        // Flash / Shake effect toggle (photosensitivity)
        [SerializeField] private Button flashEffectButton;
        [SerializeField] private Text flashEffectLabel;
        [SerializeField] private Text flashEffectValueText;

        private Coroutine typingCoroutine;
        // Assigned via Loc in UpdateLanguage() (Loc must not be called from a field initializer: it may hit Resources.Load at constructor time).
        private string previewMessage;

        private static System.Collections.Generic.Dictionary<string, Font> _legacyFontCache = new System.Collections.Generic.Dictionary<string, Font>();
        private Font GetLegacyFont(string name) {
            if (string.IsNullOrEmpty(name)) return null;
            if (_legacyFontCache.ContainsKey(name)) return _legacyFontCache[name];
            Font rawFont = Resources.Load<Font>("Fonts/" + name);
            if (rawFont != null) _legacyFontCache[name] = rawFont;
            return rawFont;
        }

        private GameObject dropdownBlocker;

        private void OnEnable()
        {
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
            UpdateVolumeTexts();
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

            if (flashEffectButton != null)
            {
                flashEffectButton.onClick.RemoveListener(OnFlashEffectClicked);
                flashEffectButton.onClick.AddListener(OnFlashEffectClicked);
            }
            if (skipHelpButton != null && skipHelpPanel != null)
            {
                EventTrigger trigger = skipHelpButton.gameObject.AddComponent<EventTrigger>();
                EventTrigger.Entry enter = new EventTrigger.Entry { eventID = EventTriggerType.PointerEnter };
                enter.callback.AddListener((data) => { skipHelpPanel.SetActive(true); skipHelpPanel.transform.SetAsLastSibling(); });
                trigger.triggers.Add(enter);
                EventTrigger.Entry exit = new EventTrigger.Entry { eventID = EventTriggerType.PointerExit };
                exit.callback.AddListener((data) => { skipHelpPanel.SetActive(false); });
                trigger.triggers.Add(exit);
            }
            
            if (dropdownBlocker == null && skipDropdownPanel != null)
            {
                dropdownBlocker = new GameObject("DropdownBlocker");
                RectTransform blockerRt = dropdownBlocker.AddComponent<RectTransform>();
                blockerRt.SetParent(skipDropdownPanel.transform.parent, false);
                blockerRt.anchorMin = new Vector2(0.5f, 0.5f);
                blockerRt.anchorMax = new Vector2(0.5f, 0.5f);
                blockerRt.sizeDelta = new Vector2(10000, 10000);
                
                Image blockerImg = dropdownBlocker.AddComponent<Image>();
                blockerImg.color = new Color(0, 0, 0, 0); // completely invisible
                
                Button blockerBtn = dropdownBlocker.AddComponent<Button>();
                blockerBtn.transition = Selectable.Transition.None;
                blockerBtn.onClick.AddListener(() => {
                    if (skipDropdownPanel != null) skipDropdownPanel.SetActive(false);
                    dropdownBlocker.SetActive(false);
                });
                
                dropdownBlocker.SetActive(false);
            }

            if (ctrlSkipButton != null)
            {
                ctrlSkipButton.onClick.RemoveAllListeners();
                ctrlSkipButton.onClick.AddListener(() => {
                    if (skipDropdownPanel != null) {
                        bool isActive = skipDropdownPanel.activeSelf;
                        skipDropdownPanel.SetActive(!isActive);
                        if (dropdownBlocker != null) dropdownBlocker.SetActive(!isActive);
                        
                        if (!isActive) {
                            if (dropdownBlocker != null) dropdownBlocker.transform.SetAsLastSibling();
                            skipDropdownPanel.transform.SetAsLastSibling();
                        }
                    }
                });
            }
            
            // Remove previous listeners just in case
            if (skipOptCtrl != null) { skipOptCtrl.onClick.RemoveAllListeners(); skipOptCtrl.onClick.AddListener(() => SetSkipKey(SettingsData.SkipKeyOption.Ctrl)); }
            if (skipOptShift != null) { skipOptShift.onClick.RemoveAllListeners(); skipOptShift.onClick.AddListener(() => SetSkipKey(SettingsData.SkipKeyOption.Shift)); }
            if (skipOptSpace != null) { skipOptSpace.onClick.RemoveAllListeners(); skipOptSpace.onClick.AddListener(() => SetSkipKey(SettingsData.SkipKeyOption.Space)); }
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
            if (bgmVolumeSlider != null) bgmVolumeSlider.onValueChanged.RemoveListener(OnBGMVolumeChanged);
            if (sfxVolumeSlider != null) sfxVolumeSlider.onValueChanged.RemoveListener(OnSFXVolumeChanged);
            if (textSpeedSlider != null) textSpeedSlider.onValueChanged.RemoveListener(OnTextSpeedChanged);
            if (autoPlaySlider != null) autoPlaySlider.onValueChanged.RemoveListener(OnAutoPlayChanged);
            if (flashEffectButton != null) flashEffectButton.onClick.RemoveListener(OnFlashEffectClicked);
        if (autoPlayInputField != null) autoPlayInputField.onEndEdit.RemoveListener(OnAutoPlayInputEdit);

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

            // Per-language texts come from the Loc table (Korean default inline; other languages in game_text.csv).
            SetText(bgmVolumeLabel, Loc.Get("ui.settings.bgm_volume", "배경음악 (BGM) 음량"));
            SetText(sfxVolumeLabel, Loc.Get("ui.settings.sfx_volume", "효과음 (SFX) 음량"));
            SetText(titleTextLabel, Loc.Get("ui.settings.title", "설정"));
            SetText(textSpeedLabel, Loc.Get("ui.settings.text_speed", "텍스트 속도"));
            SetText(autoPlayLabel, Loc.Get("ui.settings.auto_play_delay", "오토 대기 시간"));
            SetText(skipModeLabel, Loc.Get("ui.settings.skip_mode", "스킵 모드"));
            SetText(fontStyleLabel, Loc.Get("ui.settings.font", "글꼴"));
            SetText(returnToTitleLabel, Loc.Get("ui.settings.return_to_title", "타이틀로 돌아가기"));
            previewMessage = Loc.Get("ui.settings.preview_message", "텍스트 속도가 이 정도로 출력됩니다. 눈으로 확인해 보세요!");
            SetText(skipHelpText, Loc.Get("ui.settings.skip_help", "설정하신 단축키를 누르고 있으면 대사를 빠르게 넘길 수 있습니다."));
            SetText(flashEffectLabel, Loc.Get("ui.settings.flash_effect", "화면 번쩍임·흔들림"));

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
            SetFont(bgmVolumeLabel, 28, 22);
            SetFont(sfxVolumeLabel, 28, 22);
            SetFont(bgmVolumeValueText, 20, 16);
            SetFont(sfxVolumeValueText, 20, 16);
            SetFont(textSpeedLabel, 28, 22);
            SetFont(autoPlayLabel, 28, 22);
            
            SetFont(skipModeLabel, 28, 22);
            SetFont(fontStyleLabel, 28, 22);
            SetFont(flashEffectLabel, 28, 22);
            
            SetFont(ctrlSkipValueText, 20, 16);
            SetFont(fontStyleValueText, 20, 16);
            SetFont(flashEffectValueText, 20, 16);
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
        
        private void OnFlashEffectClicked()
        {
            SettingsData.EnableFlashingEffects = !SettingsData.EnableFlashingEffects;
            SettingsData.Save();
            UpdateAllLabels();
        }


        // Values are persisted by SettingsData.Save() in Hide(). Writing PlayerPrefs on every
        // drag tick caused a storage write per frame (noticeable stutter on WebGL).
        private void OnBGMVolumeChanged(float value)
        {
            SettingsData.BGMVolume = value;
            if (AudioManager.Instance != null) AudioManager.Instance.UpdateVolume();
            UpdateVolumeTexts();
        }

        private void OnSFXVolumeChanged(float value)
        {
            SettingsData.SFXVolume = value;
            if (AudioManager.Instance != null)
            {
                AudioManager.Instance.UpdateVolume();
                // Audible preview so the player can hear the new SFX level while dragging.
                if (Time.unscaledTime - lastSfxPreviewTime > 0.15f)
                {
                    lastSfxPreviewTime = Time.unscaledTime;
                    AudioManager.Instance.PlaySFX("sfx_ui_click");
                }
            }
            UpdateVolumeTexts();
        }

        private void UpdateVolumeTexts()
        {
            if (bgmVolumeValueText != null) bgmVolumeValueText.text = Mathf.RoundToInt(SettingsData.BGMVolume * 100f) + "%";
            if (sfxVolumeValueText != null) sfxVolumeValueText.text = Mathf.RoundToInt(SettingsData.SFXVolume * 100f) + "%";
        }

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
        private void SetSkipKey(SettingsData.SkipKeyOption key)
        {
            SettingsData.SkipKey = key;
            if (skipDropdownPanel != null) skipDropdownPanel.SetActive(false);
            if (dropdownBlocker != null) dropdownBlocker.SetActive(false);
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

            string fontName = FontHelper.GetFontNameForLanguage(SettingsData.Language);
            var tmpFont = FontHelper.GetTMPFont(fontName);
            if (tmpFont != null)
            {
                var allTmp = Resources.FindObjectsOfTypeAll<TMPro.TextMeshProUGUI>();
                foreach (var tmp in allTmp)
                {
                    if (tmp.gameObject.scene.name != null)
                    {
                        tmp.font = tmpFont;
                    }
                }
            }
            
            var legacyFont = GetLegacyFont(fontName);
            if (legacyFont != null)
            {
                var allLegacy = Resources.FindObjectsOfTypeAll<UnityEngine.UI.Text>();
                foreach (var txt in allLegacy)
                {
                    if (txt.gameObject.scene.name != null && txt.gameObject != fontStyleValueText.gameObject)
                    {
                        txt.font = legacyFont;
                    }
                }
            }

        }

        private void UpdateAllLabels()
        {
            if (autoPlayInputField != null) autoPlayInputField.text = SettingsData.AutoPlayDelay.ToString("0.0");
            if (flashEffectValueText != null)
            {
                bool on = SettingsData.EnableFlashingEffects;
                flashEffectValueText.text = on ? Loc.Get("ui.settings.flash_on", "켜짐") : Loc.Get("ui.settings.flash_off", "꺼짐");
            }
            if (ctrlSkipValueText != null)
            {
                string keyName = "Ctrl ▼";
                if (SettingsData.SkipKey == SettingsData.SkipKeyOption.Shift) keyName = "Shift ▼";
                else if (SettingsData.SkipKey == SettingsData.SkipKeyOption.Space) keyName = "Space ▼";
                ctrlSkipValueText.text = keyName;
            }

            if (fontStyleValueText != null)
            {
                fontStyleValueText.text = SettingsData.UseHandwritingFont
                    ? Loc.Get("ui.settings.font_handwriting", "손글씨")
                    : Loc.Get("ui.settings.font_gothic", "고딕");
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
            if (string.IsNullOrEmpty(previewMessage))
                previewMessage = Loc.Get("ui.settings.preview_message", "텍스트 속도가 이 정도로 출력됩니다. 눈으로 확인해 보세요!");
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





