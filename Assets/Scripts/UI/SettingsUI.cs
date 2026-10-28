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
        [SerializeField] private Text textSpeedValueText;
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

        // Font Size Toggle
        [SerializeField] private Button fontSizeButton;
        [SerializeField] private Text fontSizeLabel;
        [SerializeField] private Text fontSizeValueText;

        // Title / Close
        [SerializeField] private Text titleTextLabel;
        [SerializeField] private Button closeButton;
        [SerializeField] private Button returnToTitleButton;
        [SerializeField] private Button deleteDataButton;
        [SerializeField] private Text returnToTitleLabel;
        [SerializeField] private Text deleteDataLabel;

        // Legacy compat (unused but kept for SetField safety)
        [SerializeField] private Slider bgmVolumeSlider;
        [SerializeField] private Text bgmVolumeLabel;
        [SerializeField] private Slider sfxVolumeSlider;
        [SerializeField] private Text sfxVolumeLabel;
        [SerializeField] private Text bgmVolumeValueText;
        [SerializeField] private Text sfxVolumeValueText;
        [SerializeField] private Toggle fullscreenToggle;

        // Flash / Shake effect toggle (photosensitivity)
        [SerializeField] private Button flashEffectButton;
        [SerializeField] private Text flashEffectLabel;
        [SerializeField] private Text flashEffectValueText;

        // Key Bindings Customization
        [SerializeField] private Button keyBindButton;
        [SerializeField] private Text keyBindLabel;
        [SerializeField] private Text keyBindValueText;

        private Coroutine typingCoroutine;
        private GameObject _deleteConfirmPopup;
        private GameObject _keyBindPopup;
        private int _rebindingActionIndex = -1;
        private int _rebindStartFrame = -1;
        private int _lastRebindCancelFrame = -1;
        private readonly Text[] _keyBindActionLabels = new Text[5];
        private readonly Text[] _keyBindSlotTexts = new Text[5];
        private readonly Image[] _keyBindSlotBgs = new Image[5];
        private Text _keyBindTitleText;
        private Text _keyBindDescText;
        private Text _keyBindStatusText;
        private Text _keyBindResetBtnText;
        private Text _keyBindCloseBtnText;
        private Sprite _keySlotNormalSprite;
        private Sprite _keySlotWaitingSprite;

        // Assigned via Loc in UpdateLanguage() (Loc must not be called from a field initializer: it may hit Resources.Load at constructor time).
        private string previewMessage;

        private Font GetLegacyFont(string name) => FontHelper.GetFont(name);

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
            if (keyBindButton != null)
            {
                keyBindButton.onClick.RemoveListener(OnKeyBindButtonClicked);
                keyBindButton.onClick.AddListener(OnKeyBindButtonClicked);
            }
            if (skipHelpButton != null && skipHelpPanel != null)
            {
                foreach (var g in skipHelpPanel.GetComponentsInChildren<Graphic>(true))
                {
                    g.raycastTarget = false;
                }
                EventTrigger trigger = skipHelpButton.gameObject.GetComponent<EventTrigger>();
                if (trigger == null) trigger = skipHelpButton.gameObject.AddComponent<EventTrigger>();
                trigger.triggers.Clear();
                EventTrigger.Entry enter = new EventTrigger.Entry { eventID = EventTriggerType.PointerEnter };
                enter.callback.AddListener((data) => { PositionSkipHelpAboveButton(); skipHelpPanel.SetActive(true); skipHelpPanel.transform.SetAsLastSibling(); });
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
                        if (!isActive) {
                            PositionDropdownBelowButton();
                            UpdateSkipDropdownOptions();
                            if (dropdownBlocker != null) dropdownBlocker.transform.SetAsLastSibling();
                            skipDropdownPanel.transform.SetAsLastSibling();
                        }
                        skipDropdownPanel.SetActive(!isActive);
                        if (dropdownBlocker != null) dropdownBlocker.SetActive(!isActive);
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
            if (fontSizeButton != null)
            {
                fontSizeButton.onClick.RemoveListener(OnFontSizeToggled);
                fontSizeButton.onClick.AddListener(OnFontSizeToggled);
            }
            if (closeButton != null)
            {
                closeButton.onClick.AddListener(Hide);
            }
            if (returnToTitleButton != null)
            {
                returnToTitleButton.onClick.AddListener(OnReturnToTitleClicked);
            }

            if (deleteDataButton != null)
                deleteDataButton.onClick.AddListener(OnDeleteDataClicked);

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
            if (keyBindButton != null) keyBindButton.onClick.RemoveListener(OnKeyBindButtonClicked);
            if (autoPlayInputField != null) autoPlayInputField.onEndEdit.RemoveListener(OnAutoPlayInputEdit);

            if (fontStyleButton != null) fontStyleButton.onClick.RemoveListener(OnFontStyleToggled);
            if (fontSizeButton != null) fontSizeButton.onClick.RemoveListener(OnFontSizeToggled);
            if (closeButton != null) closeButton.onClick.RemoveListener(Hide);
            if (returnToTitleButton != null) returnToTitleButton.onClick.RemoveListener(OnReturnToTitleClicked);
            if (deleteDataButton != null) deleteDataButton.onClick.RemoveListener(OnDeleteDataClicked);
        }

        private void Update()
        {
            if (_keyBindPopup == null || !_keyBindPopup.activeInHierarchy || _rebindingActionIndex < 0)
                return;

            if (Time.frameCount <= _rebindStartFrame)
                return;

            var kb = UnityEngine.InputSystem.Keyboard.current;
            if (kb == null) return;

            if (kb.escapeKey.wasPressedThisFrame)
            {
                if (AudioManager.Instance != null) AudioManager.Instance.PlaySFX("sfx_ui_click");
                CancelRebinding();
                return;
            }

            foreach (var keyControl in kb.allKeys)
            {
                if (keyControl == null || !keyControl.wasPressedThisFrame) continue;
                var code = keyControl.keyCode;
                if (!IsBindableKey(code)) continue;

                var normalized = SettingsData.NormalizeKey(code);
                if (AudioManager.Instance != null) AudioManager.Instance.PlaySFX("sfx_ui_click");
                ApplyKeyBinding(_rebindingActionIndex, normalized);
                return;
            }
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
            SetText(textSpeedLabel, Loc.Get("ui.settings.text_speed", "텍스트 속도 조절"));
            SetText(autoPlayLabel, Loc.Get("ui.settings.auto_play_delay", "오토 대기 시간"));
            SetText(skipModeLabel, Loc.Get("ui.settings.skip_mode", "스킵 모드"));
            SetText(fontStyleLabel, Loc.Get("ui.settings.font", "글꼴"));
            SetText(fontSizeLabel, Loc.Get("ui.settings.font_size", "글자 크기"));
            SetText(returnToTitleLabel, Loc.Get("ui.settings.return_to_title", "타이틀로 돌아가기"));
            SetText(deleteDataLabel, Loc.Get("ui.settings.delete_data", "데이터 삭제"));
            previewMessage = Loc.Get("ui.settings.preview_message", "텍스트 속도가 이 정도로 출력됩니다. 눈으로 확인해 보세요!");
            SetText(skipHelpText, Loc.Get("ui.settings.skip_help", "설정하신 단축키를 누르고 있으면 대사를 빠르게 넘길 수 있습니다."));
            SetText(flashEffectLabel, Loc.Get("ui.settings.flash_effect", "화면 번쩍임·흔들림"));
            SetText(keyBindLabel, Loc.Get("ui.settings.key_bindings", "단축키 설정"));
            SetText(keyBindValueText, Loc.Get("ui.settings.key_customize_btn", "단축키 변경"));

            UpdateAllLabels();
            if (_keyBindPopup != null) RefreshKeyBindPopupUI();
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
            SetFont(textSpeedValueText, 20, 16);
            SetFont(autoPlayLabel, 28, 22);
            
            SetFont(skipModeLabel, 28, 22);
            SetFont(fontStyleLabel, 28, 22);
            SetFont(fontSizeLabel, 28, 22);
            SetFont(flashEffectLabel, 28, 22);
            SetFont(keyBindLabel, 28, 22);
            
            SetFont(ctrlSkipValueText, 20, 16);
            SetFont(fontStyleValueText, 20, 16);
            SetFont(fontSizeValueText, 20, 16);
            SetFont(flashEffectValueText, 20, 16);
            SetFont(keyBindValueText, 20, 16);
            float sizeMult = SettingsData.FontSizeMultiplier;
            SetFont(previewTextLabel, Mathf.RoundToInt(24 * sizeMult), Mathf.RoundToInt(20 * sizeMult));
            SetFont(skipHelpText, 20, 16);
            SetFont(returnToTitleLabel, 22, 18);
            SetFont(deleteDataLabel, 22, 18);

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
                if (returnToTitleButton != null && HalloweenVN.Core.GameManager.Instance != null)
                {
                    bool isLobby = HalloweenVN.Core.GameManager.Instance.CurrentPhase == HalloweenVN.Core.GamePhase.Lobby;
                    returnToTitleButton.gameObject.SetActive(!isLobby);
                    if (returnToTitleLabel != null) returnToTitleLabel.gameObject.SetActive(!isLobby);
                }
                settingsPanel.SetActive(true);
                if (textSpeedSlider != null) textSpeedSlider.value = SpeedToSlider(SettingsData.TextSpeed);
                if (autoPlaySlider != null) autoPlaySlider.value = SettingsData.AutoPlayDelay;
                
                UpdateAllLabels();
                PlayPreviewText();
            }
        }

        public bool TryCloseSubPanels()
        {
            bool closedAny = false;
            if (_keyBindPopup != null)
            {
                if (_rebindingActionIndex >= 0 || _lastRebindCancelFrame == Time.frameCount)
                {
                    if (_rebindingActionIndex >= 0) CancelRebinding();
                    return true;
                }
                Destroy(_keyBindPopup);
                _keyBindPopup = null;
                _rebindingActionIndex = -1;
                closedAny = true;
            }
            if (_deleteConfirmPopup != null)
            {
                Destroy(_deleteConfirmPopup);
                _deleteConfirmPopup = null;
                closedAny = true;
            }
            if (skipDropdownPanel != null && skipDropdownPanel.activeSelf)
            {
                skipDropdownPanel.SetActive(false);
                if (dropdownBlocker != null) dropdownBlocker.SetActive(false);
                closedAny = true;
            }
            if (skipHelpPanel != null && skipHelpPanel.activeSelf)
            {
                skipHelpPanel.SetActive(false);
                closedAny = true;
            }
            return closedAny;
        }

        public void Hide()
        {
            if (_keyBindPopup != null)
            {
                Destroy(_keyBindPopup);
                _keyBindPopup = null;
                _rebindingActionIndex = -1;
            }
            TryCloseSubPanels();
            SettingsData.Save();
            if (settingsPanel != null) settingsPanel.SetActive(false);
            if (typingCoroutine != null)
            {
                StopCoroutine(typingCoroutine);
                typingCoroutine = null;
            }
        }

        private void OnReturnToTitleClicked()
        {
            Hide();
            if (HalloweenVN.Dialogue.DialogueManager.Instance != null)
                HalloweenVN.Dialogue.DialogueManager.Instance.EndDialogue();
            if (HalloweenVN.Core.GameManager.Instance != null)
                HalloweenVN.Core.GameManager.Instance.ChangePhase(HalloweenVN.Core.GamePhase.Lobby);
            // The Lobby phase owns starting its music; do not stop it here.
        } // --- Callbacks ---
        
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
            }
            UpdateVolumeTexts();
        }

        private void UpdateVolumeTexts()
        {
            if (bgmVolumeValueText != null) bgmVolumeValueText.text = Mathf.RoundToInt(SettingsData.BGMVolume * 100f) + "%";
            if (sfxVolumeValueText != null) sfxVolumeValueText.text = Mathf.RoundToInt(SettingsData.SFXVolume * 100f) + "%";
            if (textSpeedValueText != null) textSpeedValueText.text = Mathf.RoundToInt(SpeedToSlider(SettingsData.TextSpeed) * 100f) + "%";
        }

        private void OnTextSpeedChanged(float val)
        {
            SettingsData.TextSpeed = SliderToSpeed(val);
            if (textSpeedValueText != null) textSpeedValueText.text = Mathf.RoundToInt(val * 100f) + "%";
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
            if (_keyBindPopup != null) RefreshKeyBindPopupUI();
        }

        private void OnFontSizeToggled()
        {
            SettingsData.FontSizeLevel = (SettingsData.FontSizeLevel + 1) % 3;
            SettingsData.Save();
            UpdateLanguage();
            var dialogue = Object.FindAnyObjectByType<DialogueUI>(FindObjectsInactive.Include);
            if (dialogue != null) dialogue.UpdateLanguage();
            var extra = Object.FindAnyObjectByType<ExtraUI>(FindObjectsInactive.Include);
            if (extra != null) extra.UpdateLanguage();
            var backlog = Object.FindAnyObjectByType<BacklogUI>(FindObjectsInactive.Include);
            if (backlog != null && backlog.IsOpen) backlog.ShowBacklog();
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
                var allTmp = Object.FindObjectsByType<TMPro.TextMeshProUGUI>(FindObjectsInactive.Include, FindObjectsSortMode.None);
                foreach (var tmp in allTmp)
                {
                    if (tmp != null)
                    {
                        tmp.font = tmpFont;
                    }
                }
            }
            
            var legacyFont = GetLegacyFont(fontName);
            if (legacyFont != null)
            {
                var allLegacy = Object.FindObjectsByType<UnityEngine.UI.Text>(FindObjectsInactive.Include, FindObjectsSortMode.None);
                foreach (var txt in allLegacy)
                {
                    if (txt != null && txt.gameObject != fontStyleValueText.gameObject)
                    {
                        txt.font = legacyFont;
                    }
                }
            }

        }

        private void UpdateAllLabels()
        {
            UpdateVolumeTexts();
            if (autoPlayInputField != null) autoPlayInputField.text = SettingsData.AutoPlayDelay.ToString("0.0");
            if (flashEffectValueText != null)
            {
                bool on = SettingsData.EnableFlashingEffects;
                flashEffectValueText.text = on ? Loc.Get("ui.settings.flash_on", "켜짐") : Loc.Get("ui.settings.flash_off", "꺼짐");
            }
            if (ctrlSkipValueText != null)
            {
                ctrlSkipValueText.text = SettingsData.GetKeyDisplayName(SettingsData.SkipKeyBinding) + " ▼";
            }
            if (keyBindValueText != null)
            {
                keyBindValueText.text = Loc.Get("ui.settings.key_customize_btn", "단축키 변경");
            }

            if (fontStyleValueText != null)
            {
                fontStyleValueText.text = SettingsData.UseHandwritingFont
                    ? Loc.Get("ui.settings.font_handwriting", "손글씨")
                    : Loc.Get("ui.settings.font_gothic", "고딕");
            }

            if (fontSizeValueText != null)
            {
                switch (SettingsData.FontSizeLevel)
                {
                    case 1:
                        fontSizeValueText.text = Loc.Get("ui.settings.font_size_large", "크게 (120%)");
                        break;
                    case 2:
                        fontSizeValueText.text = Loc.Get("ui.settings.font_size_xlarge", "매우 크게 (140%)");
                        break;
                    default:
                        fontSizeValueText.text = Loc.Get("ui.settings.font_size_normal", "보통 (100%)");
                        break;
                }
            }

            UpdateSkipDropdownOptions();
        }

        private void PositionSkipHelpAboveButton()
        {
            if (skipHelpButton == null || skipHelpPanel == null) return;
            RectTransform btnRt = skipHelpButton.GetComponent<RectTransform>();
            RectTransform helpRt = skipHelpPanel.GetComponent<RectTransform>();
            RectTransform parentRt = skipHelpPanel.transform.parent as RectTransform;
            if (btnRt == null || helpRt == null || parentRt == null) return;

            Vector3[] corners = new Vector3[4];
            btnRt.GetWorldCorners(corners); // 1: top-left, 2: top-right
            Vector3 topCenter = (corners[1] + corners[2]) * 0.5f;

            Vector2 localPoint;
            RectTransformUtility.ScreenPointToLocalPointInRectangle(
                parentRt,
                RectTransformUtility.WorldToScreenPoint(null, topCenter),
                null,
                out localPoint
            );

            helpRt.anchoredPosition = new Vector2(0f, localPoint.y + 42f);
        }

        private void PositionDropdownBelowButton()
        {
            if (ctrlSkipButton == null || skipDropdownPanel == null) return;
            RectTransform btnRt = ctrlSkipButton.GetComponent<RectTransform>();
            RectTransform dropRt = skipDropdownPanel.GetComponent<RectTransform>();
            RectTransform parentRt = skipDropdownPanel.transform.parent as RectTransform;
            if (btnRt == null || dropRt == null || parentRt == null) return;

            Vector3[] corners = new Vector3[4];
            btnRt.GetWorldCorners(corners); // 0: bottom-left, 3: bottom-right
            Vector3 bottomCenter = (corners[0] + corners[3]) * 0.5f;

            Vector2 localPoint;
            RectTransformUtility.ScreenPointToLocalPointInRectangle(
                parentRt,
                RectTransformUtility.WorldToScreenPoint(null, bottomCenter),
                null,
                out localPoint
            );

            dropRt.pivot = new Vector2(0.5f, 1f); // Top-center pivot: expands downwards
            dropRt.anchoredPosition = new Vector2(localPoint.x, localPoint.y - 4f); // 4px gap below button
        }

        private void UpdateSkipDropdownOptions()
        {
            void StyleOption(Button optBtn, string label, bool isSel)
            {
                if (optBtn == null) return;
                Text t = optBtn.GetComponentInChildren<Text>();
                if (t != null)
                {
                    t.text = isSel ? "◆  " + label : "    " + label;
                    t.color = isSel ? HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange : new Color32(235, 230, 248, 255);
                    t.fontStyle = isSel ? FontStyle.Bold : FontStyle.Normal;
                }
                Transform borderTr = optBtn.transform.Find("Border");
                if (borderTr != null)
                {
                    Image borderImg = borderTr.GetComponent<Image>();
                    if (borderImg != null)
                    {
                        borderImg.color = isSel ? new Color32(235, 140, 45, 255) : new Color32(135, 95, 175, 240);
                    }
                }
            }

            var skipKey = SettingsData.SkipKeyBinding;
            StyleOption(skipOptCtrl, "Ctrl", skipKey == UnityEngine.InputSystem.Key.LeftCtrl || skipKey == UnityEngine.InputSystem.Key.RightCtrl);
            StyleOption(skipOptShift, "Shift", skipKey == UnityEngine.InputSystem.Key.LeftShift || skipKey == UnityEngine.InputSystem.Key.RightShift);
            StyleOption(skipOptSpace, "Space", skipKey == UnityEngine.InputSystem.Key.Space);
        }

        // --- Key Bindings Customization Popup ---

        private void OnKeyBindButtonClicked()
        {
            if (skipDropdownPanel != null && skipDropdownPanel.activeSelf)
            {
                skipDropdownPanel.SetActive(false);
                if (dropdownBlocker != null) dropdownBlocker.SetActive(false);
            }
            ShowKeyBindingsPopup();
        }

        private static string GetActionLabel(int index)
        {
            switch (index)
            {
                case 0: return Loc.Get("ui.settings.key_action_advance", "대사 진행");
                case 1: return Loc.Get("ui.settings.key_action_skip", "빠른 스킵 (누르기)");
                case 2: return Loc.Get("ui.settings.key_action_auto", "자동 재생 (AUTO)");
                case 3: return Loc.Get("ui.settings.key_action_backlog", "대화 기록 (LOG)");
                case 4: return Loc.Get("ui.settings.key_action_hide_ui", "UI 숨기기");
                default: return "";
            }
        }

        private static UnityEngine.InputSystem.Key GetActionKey(int index)
        {
            switch (index)
            {
                case 0: return SettingsData.AdvanceKey;
                case 1: return SettingsData.SkipKeyBinding;
                case 2: return SettingsData.AutoPlayKey;
                case 3: return SettingsData.BacklogKey;
                case 4: return SettingsData.HideUiKey;
                default: return UnityEngine.InputSystem.Key.None;
            }
        }

        private static void SetActionKey(int index, UnityEngine.InputSystem.Key key)
        {
            switch (index)
            {
                case 0: SettingsData.AdvanceKey = key; break;
                case 1: SettingsData.SkipKeyBinding = key; break;
                case 2: SettingsData.AutoPlayKey = key; break;
                case 3: SettingsData.BacklogKey = key; break;
                case 4: SettingsData.HideUiKey = key; break;
            }
        }

        private static bool IsBindableKey(UnityEngine.InputSystem.Key key)
        {
            if (key == UnityEngine.InputSystem.Key.None ||
                key == UnityEngine.InputSystem.Key.Escape ||
                key == UnityEngine.InputSystem.Key.LeftMeta ||
                key == UnityEngine.InputSystem.Key.RightMeta ||
                key == UnityEngine.InputSystem.Key.ContextMenu ||
                key == UnityEngine.InputSystem.Key.CapsLock ||
                key == UnityEngine.InputSystem.Key.NumLock ||
                key == UnityEngine.InputSystem.Key.ScrollLock ||
                key == UnityEngine.InputSystem.Key.PrintScreen ||
                key == UnityEngine.InputSystem.Key.Pause)
            {
                return false;
            }
            return true;
        }

        private void StartRebinding(int actionIndex)
        {
            _rebindingActionIndex = actionIndex;
            _rebindStartFrame = Time.frameCount;
            if (_keyBindStatusText != null)
            {
                _keyBindStatusText.text = Loc.Get("ui.settings.key_waiting_hint", "원하는 키를 눌러주세요. (ESC 키를 누르면 취소됩니다)");
                _keyBindStatusText.color = HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange;
            }
            RefreshKeyBindPopupUI();
        }

        private void CancelRebinding()
        {
            _rebindingActionIndex = -1;
            _lastRebindCancelFrame = Time.frameCount;
            if (_keyBindStatusText != null)
            {
                _keyBindStatusText.text = Loc.Get("ui.settings.key_canceled", "단축키 변경이 취소되었습니다.");
                _keyBindStatusText.color = new Color32(195, 180, 215, 255);
            }
            RefreshKeyBindPopupUI();
        }

        private void ApplyKeyBinding(int actionIndex, UnityEngine.InputSystem.Key newKey)
        {
            var oldKey = GetActionKey(actionIndex);
            int conflictIndex = -1;
            for (int i = 0; i < 5; i++)
            {
                if (i == actionIndex) continue;
                if (GetActionKey(i) == newKey)
                {
                    conflictIndex = i;
                    break;
                }
            }

            if (conflictIndex >= 0)
            {
                SetActionKey(conflictIndex, oldKey);
            }
            SetActionKey(actionIndex, newKey);
            SettingsData.Save();

            _rebindingActionIndex = -1;
            if (_keyBindStatusText != null)
            {
                if (conflictIndex >= 0)
                {
                    _keyBindStatusText.text = Loc.Format("ui.settings.key_swapped", "'{0}' 키가 중복되어 '{1}' 항목과 교체되었습니다.", SettingsData.GetKeyDisplayName(newKey), GetActionLabel(conflictIndex));
                }
                else
                {
                    _keyBindStatusText.text = Loc.Format("ui.settings.key_changed", "'{0}' 단축키가 [{1}] 키로 변경되었습니다.", GetActionLabel(actionIndex), SettingsData.GetKeyDisplayName(newKey));
                }
                _keyBindStatusText.color = new Color32(235, 225, 250, 255);
            }

            UpdateAllLabels();
            RefreshKeyBindPopupUI();
        }

        private void ShowKeyBindingsPopup()
        {
            if (_keyBindPopup != null) Destroy(_keyBindPopup);
            _rebindingActionIndex = -1;

            Transform parent = settingsPanel != null ? settingsPanel.transform : transform;
            string fontName = FontHelper.GetFontNameForLanguage(SettingsData.Language);
            Font f = GetLegacyFont(fontName);
            bool isGothic = !SettingsData.UseHandwritingFont;

            _keyBindPopup = HalloweenVN.UI.Theme.UIHelper.CreateUIObject("KeyBindPopup", parent);
            HalloweenVN.UI.Theme.UIHelper.StretchFull(_keyBindPopup.GetComponent<RectTransform>());
            HalloweenVN.UI.Theme.UIHelper.AddImage(_keyBindPopup, new Color(0, 0, 0, 0.78f));

            Button bgCancel = _keyBindPopup.AddComponent<Button>();
            bgCancel.transition = Selectable.Transition.None;
            bgCancel.onClick.AddListener(() => {
                if (_rebindingActionIndex >= 0)
                {
                    CancelRebinding();
                    return;
                }
                if (_keyBindPopup != null)
                {
                    Destroy(_keyBindPopup);
                    _keyBindPopup = null;
                }
            });

            Sprite panelSprite = HalloweenVN.UI.Theme.UIHelper.CreateRoundedRectSprite(
                16, 2, new Color32(24, 15, 38, 252), HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange);
            _keySlotNormalSprite = HalloweenVN.UI.Theme.UIHelper.CreateRoundedRectSprite(
                8, 2, new Color32(58, 38, 86, 255), new Color32(150, 105, 195, 235));
            _keySlotWaitingSprite = HalloweenVN.UI.Theme.UIHelper.CreateRoundedRectSprite(
                8, 2, new Color32(115, 52, 22, 255), HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange);
            Sprite rowBgSprite = HalloweenVN.UI.Theme.UIHelper.CreateRoundedRectSprite(
                10, 1, new Color32(38, 24, 58, 210), new Color32(95, 65, 135, 130));

            GameObject panel = HalloweenVN.UI.Theme.UIHelper.CreateUIObject("KeyBindModalPanel", _keyBindPopup.transform);
            RectTransform panelRt = panel.GetComponent<RectTransform>();
            HalloweenVN.UI.Theme.UIHelper.SetAnchors(panelRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            panelRt.sizeDelta = new Vector2(680, 560);
            Image panelImg = HalloweenVN.UI.Theme.UIHelper.AddImage(panel, Color.white, panelSprite);
            panelImg.type = Image.Type.Sliced;

            // Prevent clicks inside the modal from triggering bgCancel
            Button panelBlockBtn = panel.AddComponent<Button>();
            panelBlockBtn.transition = Selectable.Transition.None;
            panelBlockBtn.onClick.AddListener(() => {
                if (_rebindingActionIndex >= 0) CancelRebinding();
            });

            Text MakeLabel(string objName, Transform trParent, string text, Vector2 anchoredPos, Vector2 size, int defaultSize, int gothicSize, Color color, TextAnchor align)
            {
                GameObject obj = HalloweenVN.UI.Theme.UIHelper.CreateUIObject(objName, trParent);
                RectTransform rt = obj.GetComponent<RectTransform>();
                HalloweenVN.UI.Theme.UIHelper.SetAnchors(rt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
                rt.anchoredPosition = anchoredPos;
                rt.sizeDelta = size;
                Text t = obj.AddComponent<Text>();
                if (f != null) t.font = f;
                t.text = text;
                t.fontSize = isGothic ? gothicSize : defaultSize;
                t.color = color;
                t.alignment = align;
                t.horizontalOverflow = HorizontalWrapMode.Wrap;
                t.verticalOverflow = VerticalWrapMode.Overflow;
                t.raycastTarget = false;
                obj.AddComponent<LegacyTextFontFallback>();
                return t;
            }

            // Title & Subtitle
            _keyBindTitleText = MakeLabel(
                "Title", panel.transform,
                Loc.Get("ui.settings.key_popup_title", "단축키 커스텀 설정"),
                new Vector2(0, 232), new Vector2(580, 44), 34, 26,
                HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange, TextAnchor.MiddleCenter);
            _keyBindTitleText.fontStyle = FontStyle.Bold;

            _keyBindDescText = MakeLabel(
                "Desc", panel.transform,
                Loc.Get("ui.settings.key_popup_desc", "변경할 항목의 버튼을 누른 뒤 원하는 키를 입력해 주세요. (ESC: 취소)"),
                new Vector2(0, 192), new Vector2(600, 30), 19, 15,
                new Color32(195, 180, 215, 255), TextAnchor.MiddleCenter);

            // Top-right Close (X) Button
            GameObject xBtnObj = HalloweenVN.UI.Theme.UIHelper.CreateUIObject("CloseXBtn", panel.transform);
            RectTransform xBtnRt = xBtnObj.GetComponent<RectTransform>();
            HalloweenVN.UI.Theme.UIHelper.SetAnchors(xBtnRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            xBtnRt.anchoredPosition = new Vector2(304, 244);
            xBtnRt.sizeDelta = new Vector2(38, 38);
            Sprite xBtnSprite = HalloweenVN.UI.Theme.UIHelper.CreateRoundedRectSprite(10, 2, new Color32(60, 35, 85, 255), HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange);
            Image xBtnImg = HalloweenVN.UI.Theme.UIHelper.AddImage(xBtnObj, Color.white, xBtnSprite);
            xBtnImg.type = Image.Type.Sliced;
            Button xBtn = xBtnObj.AddComponent<Button>();
            xBtnObj.AddComponent<UIHoverSound>();
            MakeLabel("XLabel", xBtnObj.transform, "×", Vector2.zero, new Vector2(38, 38), 26, 22, HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange, TextAnchor.MiddleCenter);
            xBtn.onClick.AddListener(() => {
                if (_keyBindPopup != null)
                {
                    Destroy(_keyBindPopup);
                    _keyBindPopup = null;
                    _rebindingActionIndex = -1;
                }
            });

            // 5 Key Binding Rows
            float startY = 130f;
            float rowSpacing = 58f;
            for (int i = 0; i < 5; i++)
            {
                int idx = i;
                float y = startY - i * rowSpacing;

                GameObject rowObj = HalloweenVN.UI.Theme.UIHelper.CreateUIObject("KeyRow_" + i, panel.transform);
                RectTransform rowRt = rowObj.GetComponent<RectTransform>();
                HalloweenVN.UI.Theme.UIHelper.SetAnchors(rowRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
                rowRt.anchoredPosition = new Vector2(0, y);
                rowRt.sizeDelta = new Vector2(580, 48);
                Image rowImg = HalloweenVN.UI.Theme.UIHelper.AddImage(rowObj, Color.white, rowBgSprite);
                rowImg.type = Image.Type.Sliced;
                rowImg.raycastTarget = false;

                _keyBindActionLabels[i] = MakeLabel(
                    "ActionLabel", rowObj.transform,
                    GetActionLabel(i),
                    new Vector2(-125, 0), new Vector2(280, 44), 24, 19,
                    HalloweenVN.UI.Theme.HalloweenTheme.TextPrimary, TextAnchor.MiddleLeft);

                GameObject slotBtnObj = HalloweenVN.UI.Theme.UIHelper.CreateUIObject("KeySlotBtn", rowObj.transform);
                RectTransform slotRt = slotBtnObj.GetComponent<RectTransform>();
                HalloweenVN.UI.Theme.UIHelper.SetAnchors(slotRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
                slotRt.anchoredPosition = new Vector2(145, 0);
                slotRt.sizeDelta = new Vector2(240, 38);
                Image slotBg = HalloweenVN.UI.Theme.UIHelper.AddImage(slotBtnObj, Color.white, _keySlotNormalSprite);
                slotBg.type = Image.Type.Sliced;
                _keyBindSlotBgs[i] = slotBg;

                Button slotBtn = slotBtnObj.AddComponent<Button>();
                slotBtnObj.AddComponent<UIHoverSound>();
                _keyBindSlotTexts[i] = MakeLabel(
                    "SlotText", slotBtnObj.transform,
                    SettingsData.GetKeyDisplayName(GetActionKey(i)),
                    Vector2.zero, new Vector2(230, 36), 21, 17,
                    Color.white, TextAnchor.MiddleCenter);

                slotBtn.onClick.AddListener(() => {
                    if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
                    StartRebinding(idx);
                });
            }

            // Status / Feedback line
            _keyBindStatusText = MakeLabel(
                "StatusText", panel.transform,
                "",
                new Vector2(0, -168), new Vector2(600, 28), 18, 15,
                new Color32(195, 180, 215, 255), TextAnchor.MiddleCenter);

            // Bottom Action Buttons: Reset to Defaults & Close/Confirm
            (Button btn, Text txt) MakeActionBtn(string name, string label, Vector2 pos, Color32 bgCol, Color32 borderCol)
            {
                GameObject btnObj = HalloweenVN.UI.Theme.UIHelper.CreateUIObject(name, panel.transform);
                RectTransform rt = btnObj.GetComponent<RectTransform>();
                HalloweenVN.UI.Theme.UIHelper.SetAnchors(rt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
                rt.anchoredPosition = pos;
                rt.sizeDelta = new Vector2(210, 44);
                Sprite bSprite = HalloweenVN.UI.Theme.UIHelper.CreateRoundedRectSprite(8, 2, bgCol, borderCol);
                Image bImg = HalloweenVN.UI.Theme.UIHelper.AddImage(btnObj, Color.white, bSprite);
                bImg.type = Image.Type.Sliced;

                Button b = btnObj.AddComponent<Button>();
                btnObj.AddComponent<UIHoverSound>();
                Text t = MakeLabel("Label", btnObj.transform, label, Vector2.zero, new Vector2(200, 42), 22, 18, Color.white, TextAnchor.MiddleCenter);
                return (b, t);
            }

            var resetTuple = MakeActionBtn(
                "ResetDefaultBtn",
                Loc.Get("ui.settings.key_reset_default", "기본값 복원"),
                new Vector2(-120, -224),
                new Color32(72, 42, 102, 255),
                new Color32(165, 120, 215, 235));
            _keyBindResetBtnText = resetTuple.txt;
            resetTuple.btn.onClick.AddListener(() => {
                if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
                _rebindingActionIndex = -1;
                SettingsData.ResetKeyBindings();
                UpdateAllLabels();
                if (_keyBindStatusText != null)
                {
                    _keyBindStatusText.text = Loc.Get("ui.settings.key_reset_done", "기본 단축키로 복원되었습니다.");
                    _keyBindStatusText.color = new Color32(235, 225, 250, 255);
                }
                RefreshKeyBindPopupUI();
            });

            var confirmTuple = MakeActionBtn(
                "ConfirmCloseBtn",
                Loc.Get("ui.settings.key_close", "확인"),
                new Vector2(120, -224),
                new Color32(195, 95, 25, 255),
                HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange);
            _keyBindCloseBtnText = confirmTuple.txt;
            confirmTuple.btn.onClick.AddListener(() => {
                if (_keyBindPopup != null)
                {
                    Destroy(_keyBindPopup);
                    _keyBindPopup = null;
                    _rebindingActionIndex = -1;
                }
            });

            RefreshKeyBindPopupUI();
        }

        private void RefreshKeyBindPopupUI()
        {
            if (_keyBindPopup == null) return;

            if (_keyBindTitleText != null)
                _keyBindTitleText.text = Loc.Get("ui.settings.key_popup_title", "단축키 커스텀 설정");
            if (_keyBindDescText != null)
                _keyBindDescText.text = Loc.Get("ui.settings.key_popup_desc", "변경할 항목의 버튼을 누른 뒤 원하는 키를 입력해 주세요. (ESC: 취소)");
            if (_keyBindResetBtnText != null)
                _keyBindResetBtnText.text = Loc.Get("ui.settings.key_reset_default", "기본값 복원");
            if (_keyBindCloseBtnText != null)
                _keyBindCloseBtnText.text = Loc.Get("ui.settings.key_close", "확인");

            for (int i = 0; i < 5; i++)
            {
                if (_keyBindActionLabels[i] != null)
                {
                    _keyBindActionLabels[i].text = GetActionLabel(i);
                }
                bool isWaiting = (_rebindingActionIndex == i);
                if (_keyBindSlotBgs[i] != null)
                {
                    _keyBindSlotBgs[i].sprite = isWaiting ? _keySlotWaitingSprite : _keySlotNormalSprite;
                }
                if (_keyBindSlotTexts[i] != null)
                {
                    if (isWaiting)
                    {
                        _keyBindSlotTexts[i].text = Loc.Get("ui.settings.key_waiting", "키 입력 대기중...");
                        _keyBindSlotTexts[i].color = HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange;
                        _keyBindSlotTexts[i].fontStyle = FontStyle.Bold;
                    }
                    else
                    {
                        _keyBindSlotTexts[i].text = SettingsData.GetKeyDisplayName(GetActionKey(i));
                        _keyBindSlotTexts[i].color = Color.white;
                        _keyBindSlotTexts[i].fontStyle = FontStyle.Normal;
                    }
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

        private void OnDeleteDataClicked()
        {
            if (_deleteConfirmPopup != null) Destroy(_deleteConfirmPopup);
            Transform parent = settingsPanel != null ? settingsPanel.transform : transform;

            string fontName = FontHelper.GetFontNameForLanguage(SettingsData.Language);
            Font f = GetLegacyFont(fontName);
            bool isGothic = !SettingsData.UseHandwritingFont;

            _deleteConfirmPopup = HalloweenVN.UI.Theme.UIHelper.CreateUIObject("DeleteConfirmPopup", parent);
            HalloweenVN.UI.Theme.UIHelper.StretchFull(_deleteConfirmPopup.GetComponent<RectTransform>());
            HalloweenVN.UI.Theme.UIHelper.AddImage(_deleteConfirmPopup, new Color(0, 0, 0, 0.72f));
            Button bgCancel = _deleteConfirmPopup.AddComponent<Button>();
            bgCancel.transition = Selectable.Transition.None;
            bgCancel.onClick.AddListener(() => { if (_deleteConfirmPopup != null) { Destroy(_deleteConfirmPopup); _deleteConfirmPopup = null; } });

            Sprite panelSprite = HalloweenVN.UI.Theme.UIHelper.CreateRoundedRectSprite(14, 2, new Color32(28, 16, 42, 250), new Color32(235, 95, 95, 220));

            GameObject panel = HalloweenVN.UI.Theme.UIHelper.CreateUIObject("ConfirmPanel", _deleteConfirmPopup.transform);
            RectTransform panelRt = panel.GetComponent<RectTransform>();
            HalloweenVN.UI.Theme.UIHelper.SetAnchors(panelRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            panelRt.sizeDelta = new Vector2(540, 230);
            Image panelImg = HalloweenVN.UI.Theme.UIHelper.AddImage(panel, Color.white, panelSprite);
            panelImg.type = Image.Type.Sliced;

            // Block clicks inside the panel from closing the popup via bgCancel
            Button panelBlockBtn = panel.AddComponent<Button>();
            panelBlockBtn.transition = Selectable.Transition.None;

            GameObject msgObj = HalloweenVN.UI.Theme.UIHelper.CreateUIObject("Message", panel.transform);
            RectTransform msgRt = msgObj.GetComponent<RectTransform>();
            HalloweenVN.UI.Theme.UIHelper.SetAnchors(msgRt, new Vector2(0.5f, 1f), new Vector2(0.5f, 1f), new Vector2(0.5f, 1f));
            msgRt.anchoredPosition = new Vector2(0, -26);
            msgRt.sizeDelta = new Vector2(490, 100);
            Text msgTxt = msgObj.AddComponent<Text>();
            if (f != null) msgTxt.font = f;
            msgTxt.text = Loc.Get("ui.settings.delete_data_confirm", "정말로 데이터를 삭제하시겠습니까?\n(저장된 진행 내역이 모두 초기화됩니다)");
            msgTxt.fontSize = isGothic ? 20 : 25;
            msgTxt.lineSpacing = 1.2f;
            msgTxt.color = Color.white;
            msgTxt.alignment = TextAnchor.MiddleCenter;
            msgTxt.horizontalOverflow = HorizontalWrapMode.Wrap;
            msgTxt.verticalOverflow = VerticalWrapMode.Overflow;
            msgTxt.raycastTarget = false;
            msgObj.AddComponent<LegacyTextFontFallback>();

            Button MakeBtn(string name, string label, Vector2 pos, Color32 bgColor, Color32 borderColor)
            {
                GameObject btnObj = HalloweenVN.UI.Theme.UIHelper.CreateUIObject(name, panel.transform);
                RectTransform rt = btnObj.GetComponent<RectTransform>();
                HalloweenVN.UI.Theme.UIHelper.SetAnchors(rt, new Vector2(0.5f, 0f), new Vector2(0.5f, 0f), new Vector2(0.5f, 0f));
                rt.anchoredPosition = pos;
                rt.sizeDelta = new Vector2(148, 46);
                Sprite btnSprite = HalloweenVN.UI.Theme.UIHelper.CreateRoundedRectSprite(8, 2, bgColor, borderColor);
                Image bImg = HalloweenVN.UI.Theme.UIHelper.AddImage(btnObj, Color.white, btnSprite);
                bImg.type = Image.Type.Sliced;

                Button b = btnObj.AddComponent<Button>();
                btnObj.AddComponent<UIHoverSound>();

                GameObject txtObj = HalloweenVN.UI.Theme.UIHelper.CreateUIObject("Label", btnObj.transform);
                HalloweenVN.UI.Theme.UIHelper.StretchFull(txtObj.GetComponent<RectTransform>());
                Text t = txtObj.AddComponent<Text>();
                if (f != null) t.font = f;
                t.text = label;
                t.fontSize = isGothic ? 18 : 24;
                t.color = Color.white;
                t.alignment = TextAnchor.MiddleCenter;
                t.raycastTarget = false;
                txtObj.AddComponent<LegacyTextFontFallback>();
                return b;
            }

            Button yesBtn = MakeBtn("YesBtn", Loc.Get("ui.common.yes", "예"), new Vector2(-86, 26), new Color32(165, 42, 50, 255), new Color32(235, 95, 95, 255));
            Button noBtn = MakeBtn("NoBtn", Loc.Get("ui.common.no", "아니오"), new Vector2(86, 26), new Color32(55, 35, 78, 255), new Color32(140, 100, 180, 190));

            yesBtn.onClick.AddListener(() => {
                if (_deleteConfirmPopup != null) { Destroy(_deleteConfirmPopup); _deleteConfirmPopup = null; }
                ExecuteDeleteData();
            });
            noBtn.onClick.AddListener(() => {
                if (_deleteConfirmPopup != null) { Destroy(_deleteConfirmPopup); _deleteConfirmPopup = null; }
            });
        }

        private void ExecuteDeleteData()
        {
            // End the dialogue before deleting so a later autosave cannot recreate it.
            if (HalloweenVN.Dialogue.DialogueManager.Instance != null)
                HalloweenVN.Dialogue.DialogueManager.Instance.EndDialogue();
            SaveManager.Delete(0);
            Hide();
            if (GameManager.Instance != null)
                GameManager.Instance.ChangePhase(GamePhase.Lobby);
        }
    }
}





