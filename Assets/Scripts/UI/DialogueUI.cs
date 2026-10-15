using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UI;
using TMPro;
using HalloweenVN.Core;
using HalloweenVN.Dialogue;
using HalloweenVN.Data;

namespace HalloweenVN.UI
{
    public enum CharacterPosition { Left = 0, Center = 1, Right = 2 }

    public class DialogueUI : MonoBehaviour
    {
        [SerializeField] private GameObject dialoguePanel;
        [SerializeField] private TextMeshProUGUI speakerNameText;
        [SerializeField] private TextMeshProUGUI dialogueText;
        [SerializeField] private Image characterImageLeft;
        [SerializeField] private Image characterImageCenter;
        [SerializeField] private Image characterImageRight;
        [SerializeField] private Image backgroundImage;

        [SerializeField] private GameObject choicePanel;
        [SerializeField] private GameObject choiceButtonPrefab;
        [SerializeField] private Transform choiceButtonContainer;
        [SerializeField] private Button autoButton;
        [SerializeField] private Button backlogButton;

        [SerializeField] private Text autoButtonText;
        [SerializeField] private Text backlogButtonText;
        [SerializeField] private GameObject nextIndicator;
        [SerializeField] private GameObject skipIndicator;
        private GameObject narratorNextIndicator;
// ═══════════ Typing & Auto ═══════════
        private BacklogUI _cachedBacklogUI;
        private SettingsUI _cachedSettingsUI;
        private WaitForSeconds _cachedNewlineDelay = new WaitForSeconds(0.15f);
        private WaitForSeconds _cachedTextDelay;

        private Coroutine typingCoroutine;
        private Coroutine autoPlayCoroutine;
        private bool isTyping;

        private float _spaceHoldTimer = 0f;

        private bool IsFastForwarding
        {
            get
            {
                if (!HalloweenVN.Core.SettingsData.IsSkipKeyPressed()) return false;
                if (HalloweenVN.Core.SettingsData.SkipKeyBinding == HalloweenVN.Core.SettingsData.AdvanceKey ||
                    HalloweenVN.Core.SettingsData.SkipKeyBinding == UnityEngine.InputSystem.Key.Enter)
                {
                    return _spaceHoldTimer >= 0.25f;
                }
                return true;
            }
        }

        private bool isAutoPlay;
        private float ctrlSkipTimer = 0f;
        private string fullText;

        // ═══════════ Character Position System (ported from old project) ═══════════
        private static readonly Color DIM_COLOR = new Color(0.5f, 0.5f, 0.55f, 1f);
        private static readonly Color ACTIVE_COLOR = Color.white;
        private const float DEFAULT_FADE_SPEED = 0.35f;
        private const float MOVE_DURATION = 0.35f;
        private const float MAX_ANIM_DELTA = 0.033f;

        private Coroutine[] _moveCoroutines = new Coroutine[3];
        private Dictionary<Image, Coroutine> _highlightCoroutines = new Dictionary<Image, Coroutine>();
        private Dictionary<Image, Coroutine> _fadeCoroutines = new Dictionary<Image, Coroutine>();
        private Dictionary<string, CharacterPosition> _activeSpeakerPositions = new Dictionary<string, CharacterPosition>();
        private List<string> _speakerOrder = new List<string>();
        private List<CharacterPosition> _tempPositionList = new List<CharacterPosition>();

        // ═══════════ Narrator ═══════════
        private TextMeshProUGUI narratorText;

        /// <summary>
        /// Lazily creates the fullscreen narrator text object.
        /// Cannot be done in Awake() because dialogueText is set via SetField() AFTER AddComponent.
        /// </summary>
        private void EnsureNarratorText()
        {
            if (narratorText != null) return;

            // Parent: fullscreen click area (Image + Button)
            GameObject narratorObj = new GameObject("NarratorText_Fullscreen");
            narratorObj.layer = LayerMask.NameToLayer("UI");
            narratorObj.transform.SetParent(transform, false);
            if (dialoguePanel != null)
            {
                // Place right after dialoguePanel so ChoicePanel and DialogueHudRoot (AUTO/LOG/SKIP) render on top
                narratorObj.transform.SetSiblingIndex(dialoguePanel.transform.GetSiblingIndex() + 1);
            }
            
            RectTransform rt = narratorObj.AddComponent<RectTransform>();
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = new Vector2(-30f, -30f);
            rt.offsetMax = new Vector2(30f, 30f);

            Image img = narratorObj.AddComponent<Image>();
            img.color = new Color(0, 0, 0, 1f); // Solid black background for monologue

            Button btn = narratorObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.None;
            // Use PointerDown to prevent drag threshold from ignoring clicks
            UnityEngine.EventSystems.EventTrigger nTrigger = narratorObj.AddComponent<UnityEngine.EventSystems.EventTrigger>();
            var nEntry = new UnityEngine.EventSystems.EventTrigger.Entry { eventID = UnityEngine.EventSystems.EventTriggerType.PointerDown };
            nEntry.callback.AddListener((data) => {
                if (data is UnityEngine.EventSystems.PointerEventData ped && ped.button != UnityEngine.EventSystems.PointerEventData.InputButton.Left) return;
                OnClick();
            });
            nTrigger.triggers.Add(nEntry);

            // Child: text label (separate GameObject to avoid Graphic conflict)
            GameObject textObj = new GameObject("NarratorLabel");
            textObj.layer = LayerMask.NameToLayer("UI");
            textObj.transform.SetParent(narratorObj.transform, false);

            RectTransform textRt = textObj.AddComponent<RectTransform>();
            textRt.anchorMin = Vector2.zero;
            textRt.anchorMax = Vector2.one;
            textRt.offsetMin = new Vector2(30f, 30f);
            textRt.offsetMax = new Vector2(-30f, -30f);
            textRt.sizeDelta = Vector2.zero;

            narratorText = textObj.AddComponent<TextMeshProUGUI>();
            narratorText.margin = new Vector4(100, 100, 100, 100);
            
            TMP_FontAsset font = null;
            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(HalloweenVN.Core.SettingsData.Language);
            font = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            
            if (font == null && dialogueText != null && dialogueText.font != null)
                font = dialogueText.font;
            if (font == null)
                font = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
            if (font == null)
                font = TMP_Settings.defaultFontAsset;
            
            if (font != null) 
            {
                narratorText.font = font;
                Debug.Log($"[DialogueUI] Assigned font: {font.name} to narratorText.");
            }
            else
            {
                Debug.LogError("[DialogueUI] Failed to assign font to narratorText!");
            }

            narratorText.fontSize = (dialogueText != null && dialogueText.fontSize > 0) ? dialogueText.fontSize : 36f;
            narratorText.color = Color.white;
            narratorText.alignment = TextAlignmentOptions.Center;
            narratorText.textWrappingMode = TextWrappingModes.Normal;
            narratorText.overflowMode = TextOverflowModes.Overflow;
            narratorText.raycastTarget = false; // let clicks pass through to parent Button

            // Typing complete indicator (▼) for fullscreen narration
            narratorNextIndicator = new GameObject("NarratorNextIndicator");
            narratorNextIndicator.layer = LayerMask.NameToLayer("UI");
            narratorNextIndicator.transform.SetParent(narratorObj.transform, false);
            RectTransform nIndRt = narratorNextIndicator.AddComponent<RectTransform>();
            nIndRt.anchorMin = new Vector2(1f, 0f);
            nIndRt.anchorMax = new Vector2(1f, 0f);
            nIndRt.pivot = new Vector2(1f, 0f);
            nIndRt.anchoredPosition = new Vector2(-90f, 80f);
            nIndRt.sizeDelta = new Vector2(40, 40);
            TextMeshProUGUI nIndTxt = narratorNextIndicator.AddComponent<TextMeshProUGUI>();
            nIndTxt.text = "▼";
            nIndTxt.fontSize = 26f;
            nIndTxt.color = HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange;
            nIndTxt.alignment = TextAlignmentOptions.Center;
            nIndTxt.raycastTarget = false;
            if (font != null) nIndTxt.font = font;
            narratorNextIndicator.SetActive(false);
            
            narratorObj.SetActive(false);
        }

        // ═══════════ Events ═══════════
        
        
        public void ClearAll()
        {
            StopAutoPlay();
            CancelSceneTransition();
            if (backgroundImage != null) backgroundImage.enabled = false;
            _currentBgPath = null;
            HideAllCharacters();
            _tempPositionList.Clear();
            
            if (dialoguePanel != null) dialoguePanel.SetActive(false);
            if (narratorText != null && narratorText.transform.parent != null) narratorText.transform.parent.gameObject.SetActive(false);
            if (autoButton != null) autoButton.gameObject.SetActive(false);
            if (backlogButton != null) backlogButton.gameObject.SetActive(false);
            if (skipIndicator != null) skipIndicator.SetActive(false);
            if (nextIndicator != null) nextIndicator.SetActive(false);
            if (narratorNextIndicator != null) narratorNextIndicator.SetActive(false);
        }

        public void UpdateLanguage()
        {
            if (backlogButtonText != null) backlogButtonText.resizeTextForBestFit = false;
            if (autoButtonText != null) autoButtonText.resizeTextForBestFit = false;
            
            // Gothic font renders visually larger than handwriting — reduce sizes
            bool isGothic = !HalloweenVN.Core.SettingsData.UseHandwritingFont;
            int btnSize = isGothic ? 24 : 32;
            float dialogueSize = isGothic ? 26f : 36f;
            float speakerSize = isGothic ? 28f : 40f;

            if (backlogButtonText != null) backlogButtonText.fontSize = btnSize;
            if (autoButtonText != null) autoButtonText.fontSize = btnSize;
            if (dialogueText != null) dialogueText.fontSize = dialogueSize;
            if (speakerNameText != null) speakerNameText.fontSize = speakerSize;
            if (narratorText != null) narratorText.fontSize = dialogueSize;

            var lang = HalloweenVN.Core.SettingsData.Language;
            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(lang);
            var font = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            if (font != null)
            {
                if (dialogueText != null) dialogueText.font = font;
                if (speakerNameText != null) speakerNameText.font = font;
                if (narratorText != null) narratorText.font = font;
            }
            string autoOff = HalloweenVN.Core.Loc.Get("ui.dialogue.auto", "오토");
            string autoOn = HalloweenVN.Core.Loc.Get("ui.dialogue.auto_on", "오토 중");
            if (backlogButtonText != null) backlogButtonText.text = HalloweenVN.Core.Loc.Get("ui.dialogue.log", "로그");
            
            if (autoButtonText != null)
            {
                autoButtonText.text = isAutoPlay ? autoOn : autoOff;
                autoButtonText.color = isAutoPlay ? Color.white : HalloweenVN.UI.Theme.HalloweenTheme.ButtonText;
            }
            UpdateAutoButtonVisuals();
        }

        private void UpdateAutoButtonVisuals()
        {
            if (autoButton == null) return;
            Color32 activeBg = new Color32(185, 75, 20, 255);
            Color32 inactiveBg = new Color32(40, 25, 60, 255);
            Color32 baseBg = isAutoPlay ? activeBg : inactiveBg;

            ColorBlock cb = autoButton.colors;
            cb.normalColor = baseBg;
            cb.highlightedColor = isAutoPlay ? new Color32(220, 100, 35, 255) : new Color32(80, 50, 115, 255);
            cb.pressedColor = isAutoPlay ? new Color32(145, 55, 12, 255) : new Color32(30, 18, 45, 255);
            cb.selectedColor = baseBg;
            autoButton.colors = cb;

            Transform borderTr = autoButton.transform.Find("Border");
            if (borderTr != null)
            {
                Image borderImg = borderTr.GetComponent<Image>();
                if (borderImg != null)
                {
                    borderImg.color = isAutoPlay
                        ? HalloweenVN.UI.Theme.HalloweenTheme.AccentOrange
                        : (Color)new Color32(90, 70, 120, 255);
                }
            }
        }
        
        private void Start()
        {
            UpdateLanguage();
        }

        private void OnEnable()
        {
            if (DialogueManager.Instance != null)
            {
                DialogueManager.Instance.OnDialogueStarted += ShowDialoguePanel;
                DialogueManager.Instance.OnDialogueEnded += HideDialoguePanel;
                DialogueManager.Instance.OnNodeDisplayed += DisplayNode;
                DialogueManager.Instance.OnChoicesDisplayed += ShowChoices;
            }
            if (autoButton != null) autoButton.onClick.AddListener(ToggleAutoPlay);
            }

        private void OnDisable()
        {
            if (DialogueManager.Instance != null)
            {
                DialogueManager.Instance.OnDialogueStarted -= ShowDialoguePanel;
                DialogueManager.Instance.OnDialogueEnded -= HideDialoguePanel;
                DialogueManager.Instance.OnNodeDisplayed -= DisplayNode;
                DialogueManager.Instance.OnChoicesDisplayed -= ShowChoices;
            }
            if (autoButton != null) autoButton.onClick.RemoveListener(ToggleAutoPlay);
            StopAutoPlay();
            CancelSceneTransition();
        }

        // ═══════════ Panel Show/Hide ═══════════
        public void ShowDialoguePanel()
        {
            isUiHidden = false;
            if (dialoguePanel != null)
                dialoguePanel.SetActive(true);
            if (autoButton != null)
                autoButton.gameObject.SetActive(true);
            if (backlogButton != null)
                backlogButton.gameObject.SetActive(true);
            ClearChoices();
            _freshDialogue = true;
            _ownersBeforeNarrator.Clear();
            _xBeforeNarrator.Clear();
            _wasNarratorLinePrev = false;

            if (DialogueManager.Instance != null && DialogueManager.Instance.CurrentDialogue != null && gameObject.activeInHierarchy)
            {
                if (_preloadCoroutine != null) StopCoroutine(_preloadCoroutine);
                _preloadCoroutine = StartCoroutine(PreloadChapterSpritesRoutine(DialogueManager.Instance.CurrentDialogue));
            }
        }

        public void HideDialoguePanel()
        {
            if (_preloadCoroutine != null)
            {
                StopCoroutine(_preloadCoroutine);
                _preloadCoroutine = null;
            }
            if (dialoguePanel != null)
                dialoguePanel.SetActive(false);
            if (autoButton != null)
                autoButton.gameObject.SetActive(false);
            if (backlogButton != null)
                backlogButton.gameObject.SetActive(false);
            if (skipIndicator != null)
                skipIndicator.SetActive(false);
            if (nextIndicator != null)
                nextIndicator.SetActive(false);
            if (narratorNextIndicator != null)
                narratorNextIndicator.SetActive(false);
            ClearChoices();
            if (DialogueManager.Instance == null || !DialogueManager.Instance.IsTransitioningChapter)
            {
                StopAutoPlay();
            }
            else
            {
                CancelAutoPlayTimer();
            }
            CancelSceneTransition();
            HideAllCharacters();
        }

        // ═══════════ Display Node ═══════════


        internal static Color GetSpeakerColor(string speaker)
        {
            if (string.IsNullOrWhiteSpace(speaker)) return HalloweenVN.UI.Theme.HalloweenTheme.TextSpeaker;
            switch (speaker.Trim())
            {
                case "세이카": return new Color32(100, 140, 255, 255); // Royal Blue (짙은 파란 머리 + 파란 눈)
                case "카스미": return new Color32(120, 200, 200, 255); // Teal (짙은 남보라 머리 + 청록색 눈동자)
                case "리나": return new Color32(110, 170, 255, 255); // Sky Blue (파란 눈 + 은색 X헤어핀)
                case "미나": return new Color32(170, 170, 255, 255); // Lavender Blue (연보라~은빛 머리 + 흰 드레스)
                case "리리스": return new Color32(180, 230, 240, 255); // Ice Cyan (은백~하늘색 숏컷 + 흰 테크웨어)
                case "하루카": return new Color32(240, 180, 210, 255); // Soft Pink (연핑크 재킷 + 흰 원피스)
                case "???": return new Color32(180, 180, 180, 255); // Grey
                default: return HalloweenVN.UI.Theme.HalloweenTheme.TextSpeaker;
            }
        }

        
        // Pooled ghost images used to fade out characters that leave while their slot image is reused
        private readonly Image[] _ghostPool = new Image[3];
        private readonly Coroutine[] _ghostCoroutines = new Coroutine[3];
        private Coroutine _preloadCoroutine;

        // Track characters on screen right before a narration (지문) line so returning characters don't re-slide as new arrivals
        private readonly HashSet<string> _ownersBeforeNarrator = new HashSet<string>();
        private readonly Dictionary<string, float> _xBeforeNarrator = new Dictionary<string, float>();
        private bool _wasNarratorLinePrev = false;

        // Last layout target assigned to each slot (-1 = empty). Used to detect interrupted slides.
        private readonly float[] _lastTargetX = { -1f, -1f, -1f };

        public void UpdateVisualsOnly(DialogueNode node, bool instant)
        {
            bool wasNarrator = !_currentlyInDialoguePanel;
            bool isNarrator = string.IsNullOrWhiteSpace(node.speaker);
            bool isNarratorNow = string.IsNullOrEmpty(node.speaker);
            bool usePanelNow = !isNarratorNow;
            string effectiveBg = !string.IsNullOrEmpty(node.backgroundSprite) ? node.backgroundSprite : _currentBgPath;
            bool isBlackBgIntro = isNarratorNow || effectiveBg == "Images/bg_black" || effectiveBg == "bg_black";

            Image[] imgs = { characterImageLeft, characterImageCenter, characterImageRight };
            bool immediate = instant;

            if (!string.IsNullOrEmpty(node.backgroundSprite) && !string.IsNullOrEmpty(_currentBgPath) && node.backgroundSprite != _currentBgPath)
            {
                _ownersBeforeNarrator.Clear();
                _xBeforeNarrator.Clear();
                _wasNarratorLinePrev = false;
            }

            // 1. Requested sprites per slot (legacy single-sprite → center)
            string[] requested = { node.characterSpriteLeft, node.characterSpriteCenter, node.characterSpriteRight };
            if (!string.IsNullOrEmpty(node.characterSprite))
            {
                requested[0] = null; requested[1] = node.characterSprite; requested[2] = null;
            }

            // 2. New owner per slot (same character listed twice — keep the first slot only)
            string[] newOwner = new string[3];
            HashSet<string> newNames = new HashSet<string>();
            for (int s = 0; s < 3; s++)
            {
                if (string.IsNullOrEmpty(requested[s])) continue;
                
                // If the sprite doesn't actually exist in the game, treat it as empty
                Sprite testSp = LoadSpriteCached(requested[s]);
                if (testSp == null)
                {
                    string fallback = null;
                    int slash = requested[s].LastIndexOf('/');
                    if (slash > 0) fallback = requested[s].Substring(0, slash) + "/기본";
                    if (fallback != null) testSp = LoadSpriteCached(fallback);
                }
                
                if (testSp == null)
                {
                    requested[s] = null;
                    continue;
                }

                string name = ExtractBaseName(requested[s]);
                if (newNames.Contains(name)) { requested[s] = null; continue; }
                newOwner[s] = name;
                newNames.Add(name);
            }

            // 3. Snapshot the previous on-screen state BEFORE touching any image.
            string[] prevOwner = new string[3];
            Dictionary<string, int> prevSlotOf = new Dictionary<string, int>();
            foreach (var kvp in _activeSpeakerPositions)
            {
                int s = (int)kvp.Value;
                Image img = imgs[s];
                if (img == null) continue;
                prevOwner[s] = kvp.Key;
                prevSlotOf[kvp.Key] = s;
            }
            float[] snapX = new float[3];
            Color[] snapColor = new Color[3];
            for (int s = 0; s < 3; s++)
            {
                if (imgs[s] == null) continue;
                RectTransform rt = imgs[s].rectTransform;
                snapX[s] = (rt.anchorMin.x + rt.anchorMax.x) / 2f;
                snapColor[s] = imgs[s].color;
            }

            bool anyoneStaying = false;
            foreach (var kvp in prevSlotOf) if (newNames.Contains(kvp.Key)) { anyoneStaying = true; break; }

            bool anyTrulyNewEntering = false;
            for (int s = 0; s < 3; s++)
            {
                if (newOwner[s] != null && !prevSlotOf.ContainsKey(newOwner[s]))
                {
                    if (!(_wasNarratorLinePrev && _ownersBeforeNarrator.Contains(newOwner[s])))
                    {
                        anyTrulyNewEntering = true;
                        break;
                    }
                }
            }

            float[] targetX = ComputeLayoutTargets(newOwner);

            // 4. Apply per slot — each slot image gets exactly one action, so characters
            //    swapping/moving slots can no longer cancel each other's fades.
            _activeSpeakerPositions.Clear();
            _speakerOrder.Clear();
            for (int s = 0; s < 3; s++)
            {
                Image img = imgs[s];
                if (img == null) continue;
                string name = newOwner[s];
                string old = prevOwner[s];

                // Previous occupant leaves the screen entirely → fade out (and gently glide out if leaving mid-dialogue)
                if (old != null && old != name && !newNames.Contains(old))
                {
                    if (!immediate) SpawnGhostFadeOut(s, img, !isNarrator);
                }

                if (name == null)
                {
                    if (old != null)
                    {
                        StopSlotCoroutines(s);
                        HideSlotImage(img);
                    }
                    continue;
                }

                _activeSpeakerPositions[name] = (CharacterPosition)s;
                _speakerOrder.Add(name);

                if (prevSlotOf.TryGetValue(name, out int from))
                {
                    // Character already on screen
                    if (from != s)
                    {
                        // Moved to a different slot: hand over the visual state and slide (no blink)
                        StopSlotCoroutines(s);
                        LoadSpriteToImage(img, requested[s]);
                        img.gameObject.SetActive(true);
                        SetCharacterAnchorX(img.rectTransform, snapX[from]);
                        img.color = snapColor[from];
                        if (snapColor[from].a < 0.999f && !immediate) StartFadeIn(img, snapColor[from].a);
                    }
                    else
                    {
                        // Same slot: expression change only
                        float curX = (img.rectTransform.anchorMin.x + img.rectTransform.anchorMax.x) / 2f;
                        bool wasMidSlide = _lastTargetX[s] >= 0f && Mathf.Abs(curX - _lastTargetX[s]) > 0.01f;
                        StopSlotCoroutines(s);
                        LoadSpriteToImage(img, requested[s]);
                        img.gameObject.SetActive(true);
                        img.color = snapColor[s];
                        if (snapColor[s].a < 0.999f && !immediate) StartFadeIn(img, snapColor[s].a);
                        else ForceOpaque(img);
                        
                        // Force snap if target position hasn't changed to prevent any unintended drifting/jumping
                        if (_lastTargetX[s] >= 0f && Mathf.Abs(_lastTargetX[s] - targetX[s]) < 0.01f)
                        {
                            SetCharacterAnchorX(img.rectTransform, targetX[s]);
                        }
                        else if (wasMidSlide) 
                        {
                            SetCharacterAnchorX(img.rectTransform, targetX[s]);
                        }
                    }

                    if (immediate)
                    {
                        StopMove(s);
                        SetCharacterAnchorX(img.rectTransform, targetX[s]);
                        ForceOpaque(img);
                    }
                    else
                    {
                        MoveCharacterTo((CharacterPosition)s, targetX[s]);
                    }
                }
                else
                {
                    // Newly entering character
                    StopSlotCoroutines(s);
                    LoadSpriteToImage(img, requested[s]);

                    float startX = targetX[s];
                    if (!immediate)
                    {
                        bool wasInRoomBeforeNarrator = _wasNarratorLinePrev && _ownersBeforeNarrator.Contains(name);
                        if (wasInRoomBeforeNarrator)
                        {
                            if (_xBeforeNarrator.TryGetValue(name, out float prevX) && Mathf.Abs(prevX - targetX[s]) > 0.01f)
                            {
                                startX = prevX;
                            }
                            else if (!anyTrulyNewEntering)
                            {
                                bool isRightSide = (s == 2) || (s == 1 && newOwner[0] != null && newOwner[2] == null);
                                float dir = isRightSide ? 1f : -1f;
                                startX = targetX[s] + dir * 0.04f;
                            }
                        }
                        else
                        {
                            bool activeSlide = node.slideIn || node.slideFromRight || anyoneStaying || (_wasNarratorLinePrev && _ownersBeforeNarrator.Count > 0);
                            float offset = activeSlide ? 0.12f : 0.06f;
                            bool isRightSide = (s == 2) || (s == 1 && newOwner[0] != null && newOwner[2] == null);
                            float dir = node.slideFromRight ? 1f : (isRightSide ? 1f : -1f);
                            startX = targetX[s] + dir * offset;
                        }
                    }
                    SetCharacterAnchorX(img.rectTransform, startX);

                    if (immediate)
                    {
                        img.gameObject.SetActive(true);
                        img.color = ACTIVE_COLOR;
                    }
                    else
                    {
                        img.color = new Color(1f, 1f, 1f, 0f);
                        StartFadeIn(img);
                        if (Mathf.Abs(startX - targetX[s]) > 0.005f) MoveCharacterTo((CharacterPosition)s, targetX[s]);
                    }
                }
            }

            if (isNarrator && !isBlackBgIntro)
            {
                if (!_wasNarratorLinePrev)
                {
                    _ownersBeforeNarrator.Clear();
                    _xBeforeNarrator.Clear();
                    foreach (var kvp in prevSlotOf)
                    {
                        _ownersBeforeNarrator.Add(kvp.Key);
                        _xBeforeNarrator[kvp.Key] = snapX[kvp.Value];
                    }
                }
                _wasNarratorLinePrev = true;
            }
            else
            {
                _wasNarratorLinePrev = false;
                _ownersBeforeNarrator.Clear();
                _xBeforeNarrator.Clear();
            }

            for (int s = 0; s < 3; s++) _lastTargetX[s] = newOwner[s] != null ? targetX[s] : -1f;

            // Dim/Highlight based on speaker
            UpdateBackground(node.backgroundSprite);
            bool instantHighlight = instant || (wasNarrator && usePanelNow);
            UpdateSpeakerHighlight(node.speaker, instantHighlight, node.command);
        }

        /// <summary>
        /// Screen X (anchor center) per slot.
        /// When 3 characters are on screen: Left=19%, Center=50%, Right=81%.
        /// When 2 characters: Left-most occupied=31%, Right-most occupied=69%.
        /// When 1 character: Occupied slot=50% (or its explicit side if needed, defaulting to 31%/50%/69%).
        /// Applies per-character visual-center compensation so asymmetric hair/veils don't skew body alignment.
        /// </summary>
        private static float[] ComputeLayoutTargets(string[] owner)
        {
            int count = 0;
            for (int s = 0; s < 3; s++)
            {
                if (owner[s] != null) count++;
            }

            float[] targets;
            if (count == 2)
            {
                targets = new float[] { 0.31f, 0.50f, 0.69f };
                bool assignedFirst = false;
                for (int s = 0; s < 3; s++)
                {
                    if (owner[s] == null) continue;
                    targets[s] = assignedFirst ? 0.69f : 0.31f;
                    assignedFirst = true;
                }
            }
            else
            {
                float leftX = count >= 3 ? 0.19f : 0.31f;
                float centerX = 0.50f;
                float rightX = count >= 3 ? 0.81f : 0.69f;
                targets = new float[] { leftX, centerX, rightX };
            }

            for (int s = 0; s < 3; s++)
            {
                if (owner[s] != null)
                {
                    targets[s] += GetCharacterVisualOffsetX(owner[s]);
                }
            }

            return targets;
        }

        /// <summary>
        /// Compensates for asymmetric sprite bounding boxes (e.g., long flowing hair or veil on one side)
        /// so that each character's actual face/torso centerline aligns with the slot's target X.
        /// </summary>
        private static float GetCharacterVisualOffsetX(string charName)
        {
            switch (charName)
            {
                case "하루카": return 0.068f;  // Long hair & skirt billow far to the right
                case "카스미": return 0.042f;  // Long dark hair flows far to the right
                case "미나":   return 0.028f;  // Wide white veil extends to the right
                case "리나":   return 0.016f;  // Hair/coat slightly wider on the right
                case "세이카": return -0.012f; // Hair/pose slightly wider on the left
                case "리리스": return -0.036f; // Jacket sleeve protrudes to the right
                default:       return 0f;
            }
        }

        private void StopMove(int slot)
        {
            if (_moveCoroutines[slot] != null)
            {
                StopCoroutine(_moveCoroutines[slot]);
                _moveCoroutines[slot] = null;
            }
        }

        private void StopSlotCoroutines(int slot)
        {
            StopMove(slot);
            Image img = GetCharacterImage((CharacterPosition)slot);
            if (img == null) return;
            if (_fadeCoroutines.TryGetValue(img, out var fc) && fc != null) StopCoroutine(fc);
            _fadeCoroutines[img] = null;
            if (_highlightCoroutines.TryGetValue(img, out var hc) && hc != null) StopCoroutine(hc);
            _highlightCoroutines[img] = null;
        }

        private static void ForceOpaque(Image img)
        {
            Color c = img.color; c.a = 1f; img.color = c;
        }

        private static void HideSlotImage(Image img)
        {
            img.gameObject.SetActive(false);
            img.color = ACTIVE_COLOR;
        }

        private void SpawnGhostFadeOut(int slot, Image source, bool slideOut)
        {
            if (source == null || !source.gameObject.activeSelf || source.sprite == null) return;
            if (slot < 0 || slot >= 3) return;

            if (_ghostCoroutines[slot] != null)
            {
                StopCoroutine(_ghostCoroutines[slot]);
                _ghostCoroutines[slot] = null;
            }

            Image gImg = _ghostPool[slot];
            if (gImg == null)
            {
                GameObject ghost = Instantiate(source.gameObject, source.transform.parent);
                ghost.name = source.gameObject.name + "_Ghost";
                gImg = ghost.GetComponent<Image>();
                if (gImg == null) { Destroy(ghost); return; }
                gImg.raycastTarget = false;
                _ghostPool[slot] = gImg;
            }

            gImg.transform.SetSiblingIndex(source.transform.GetSiblingIndex());
            gImg.sprite = source.sprite;
            gImg.preserveAspect = source.preserveAspect;
            gImg.color = source.color;

            RectTransform srcRt = source.rectTransform;
            RectTransform dstRt = gImg.rectTransform;
            dstRt.anchorMin = srcRt.anchorMin;
            dstRt.anchorMax = srcRt.anchorMax;
            dstRt.offsetMin = srcRt.offsetMin;
            dstRt.offsetMax = srcRt.offsetMax;
            dstRt.localScale = srcRt.localScale;

            gImg.gameObject.SetActive(true);
            _ghostCoroutines[slot] = StartCoroutine(GhostFadeOutRoutine(slot, gImg, slideOut));
        }

        private IEnumerator GhostFadeOutRoutine(int slot, Image img, bool slideOut)
        {
            if (img == null) yield break;
            RectTransform rt = img.rectTransform;
            float startX = (rt.anchorMin.x + rt.anchorMax.x) / 2f;
            float dir = startX > 0.5f ? 1f : -1f;
            float endX = slideOut ? (startX + dir * 0.06f) : startX;

            Color c = img.color;
            float startAlpha = c.a;

            yield return null; // wait 1 frame so synchronous node-load work does not consume fade time

            float elapsed = 0f;
            while (elapsed < DEFAULT_FADE_SPEED && img != null)
            {
                float dt = Mathf.Min(Time.unscaledDeltaTime, MAX_ANIM_DELTA) * (IsFastForwarding ? 10f : 1f);
                elapsed += dt;
                float t = Mathf.SmoothStep(0f, 1f, Mathf.Clamp01(elapsed / DEFAULT_FADE_SPEED));
                c.a = Mathf.Lerp(startAlpha, 0f, t);
                img.color = c;
                if (slideOut && rt != null)
                {
                    SetCharacterAnchorX(rt, Mathf.Lerp(startX, endX, t));
                }
                yield return null;
            }
            if (img != null) img.gameObject.SetActive(false);
            _ghostCoroutines[slot] = null;
        }

        private void DestroyGhosts()
        {
            for (int s = 0; s < 3; s++)
            {
                if (_ghostCoroutines[s] != null)
                {
                    StopCoroutine(_ghostCoroutines[s]);
                    _ghostCoroutines[s] = null;
                }
                if (_ghostPool[s] != null)
                {
                    _ghostPool[s].gameObject.SetActive(false);
                }
            }
        }

        // ═══════════ Scene (background) transition: whole screen → black → new scene ═══════════
        private bool _isTransitioningScene = false;
        private bool _sceneTransitionPastMidpoint = false;
        private bool _freshDialogue = false;
        private DialogueNode _pendingTransitionNode;
        private Coroutine _sceneTransitionCoroutine;
        private Image _sceneFadeOverlay;
        private const float SCENE_FADE_HALF = 0.4f;
        private const float SCENE_BLACK_HOLD = 0.15f;

        public void DisplayNode(DialogueNode node)
        {
            // First node of a dialogue file: chapter transitions/lobby already fade through black.
            if (_freshDialogue)
            {
                _freshDialogue = false;
                ApplyNodeVisuals(node, false);
                return;
            }

            // A transition is fading out: just swap which node gets revealed at the midpoint
            if (_sceneTransitionCoroutine != null && !_sceneTransitionPastMidpoint)
            {
                _pendingTransitionNode = node;
                return;
            }

            bool bgChanging = !string.IsNullOrEmpty(node.backgroundSprite)
                              && backgroundImage != null && backgroundImage.enabled
                              && !string.IsNullOrEmpty(_currentBgPath)
                              && node.backgroundSprite != _currentBgPath
                              && gameObject.activeInHierarchy;

            if (bgChanging)
            {
                if (_sceneTransitionCoroutine != null) StopCoroutine(_sceneTransitionCoroutine);
                _pendingTransitionNode = node;
                _sceneTransitionCoroutine = StartCoroutine(SceneTransitionRoutine());
                return;
            }

            ApplyNodeVisuals(node, false);
        }

        private IEnumerator SceneTransitionRoutine()
        {
            _isTransitioningScene = true;
            _sceneTransitionPastMidpoint = false;
            Image ov = EnsureSceneFadeOverlay();
            ov.gameObject.SetActive(true);
            ov.transform.SetAsLastSibling();

            // Fade out whole screen (continues from current alpha if a transition was interrupted)
            float a = ov.color.a;
            while (a < 1f)
            {
                a += Time.unscaledDeltaTime * (IsFastForwarding ? 10f : 1f) / SCENE_FADE_HALF;
                ov.color = new Color(0f, 0f, 0f, Mathf.SmoothStep(0f, 1f, Mathf.Clamp01(a)));
                yield return null;
            }
            ov.color = Color.black;

            // Swap scene while fully black — characters placed instantly so they're already there on reveal
            _sceneTransitionPastMidpoint = true;
            DialogueNode node = _pendingTransitionNode;
            _pendingTransitionNode = null;
            if (node != null) ApplyNodeVisuals(node, true);

            float hold = 0f;
            while (hold < SCENE_BLACK_HOLD)
            {
                hold += Time.unscaledDeltaTime * (IsFastForwarding ? 10f : 1f);
                yield return null;
            }

            // Fade back in
            a = 1f;
            while (a > 0f)
            {
                a -= Time.unscaledDeltaTime * (IsFastForwarding ? 10f : 1f) / SCENE_FADE_HALF;
                ov.color = new Color(0f, 0f, 0f, Mathf.SmoothStep(0f, 1f, Mathf.Clamp01(a)));
                yield return null;
            }
            ov.color = new Color(0f, 0f, 0f, 0f);
            ov.gameObject.SetActive(false);

            _isTransitioningScene = false;
            _sceneTransitionPastMidpoint = false;
            _sceneTransitionCoroutine = null;
        }

        private void CancelSceneTransition()
        {
            if (_sceneTransitionCoroutine != null) StopCoroutine(_sceneTransitionCoroutine);
            _sceneTransitionCoroutine = null;
            _pendingTransitionNode = null;
            _isTransitioningScene = false;
            _sceneTransitionPastMidpoint = false;
            if (_sceneFadeOverlay != null)
            {
                _sceneFadeOverlay.color = new Color(0f, 0f, 0f, 0f);
                _sceneFadeOverlay.gameObject.SetActive(false);
            }
        }

        private Image EnsureSceneFadeOverlay()
        {
            if (_sceneFadeOverlay != null) return _sceneFadeOverlay;

            Canvas parentCanvas = GetComponentInParent<Canvas>();
            Transform parent = parentCanvas != null ? parentCanvas.rootCanvas.transform : transform;

            GameObject go = new GameObject("SceneFadeOverlay", typeof(RectTransform));
            go.layer = LayerMask.NameToLayer("UI");
            go.transform.SetParent(parent, false);
            RectTransform rt = go.GetComponent<RectTransform>();
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;

            // Own sorting so it covers dialogue box, buttons and characters (ScreenTransition stays above at 999)
            Canvas c = go.AddComponent<Canvas>();
            c.overrideSorting = true;
            c.sortingOrder = 900;
            go.AddComponent<GraphicRaycaster>(); // blocks clicks on AUTO/LOG etc. during the fade

            _sceneFadeOverlay = go.AddComponent<Image>();
            _sceneFadeOverlay.color = new Color(0f, 0f, 0f, 0f);
            _sceneFadeOverlay.raycastTarget = true;
            go.SetActive(false);
            return _sceneFadeOverlay;
        }

        private void ApplyNodeVisuals(DialogueNode node, bool instantVisuals)
        {
            if (speakerNameText != null) 
            { 
                speakerNameText.text = HalloweenVN.Core.Loc.Speaker(node.speaker); 
                speakerNameText.color = GetSpeakerColor(node.speaker); 
                
                // Hide the speaker box entirely if it's a monologue (empty or just spaces)
                if (speakerNameText.transform.parent != null)
                {
                    speakerNameText.transform.parent.gameObject.SetActive(!string.IsNullOrWhiteSpace(node.speaker));
                }
            }

            // Determine which character sprites are requested
            UpdateVisualsOnly(node, instantVisuals);

            // Typing & Formatting (translation table → legacy per-node translation → Korean)
            string dlgId = DialogueManager.Instance != null ? DialogueManager.Instance.CurrentDialogueId : null;
            fullText = HalloweenVN.Core.Loc.NodeText(dlgId, node);
            bool isNarrator = string.IsNullOrEmpty(node.speaker);
            
            // Rule: Monologues with a background image use the dialogue panel.
            bool usePanel = !isNarrator;

            if (!usePanel)
            {
                EnsureNarratorText();
                fullText = "<b>" + fullText + "</b>";
            }
            else
            {
                if (dialogueText != null) dialogueText.alignment = TextAlignmentOptions.TopLeft;
            }

            _currentlyInDialoguePanel = usePanel;
            if (isUiHidden)
            {
                isUiHidden = false;
            }
            if (dialoguePanel != null) dialoguePanel.SetActive(usePanel);
            if (autoButton != null) autoButton.gameObject.SetActive(usePanel);
            if (backlogButton != null) backlogButton.gameObject.SetActive(usePanel);
            if (narratorText != null && narratorText.transform.parent != null)
            {
                narratorText.transform.parent.gameObject.SetActive(!usePanel);
            }

            TextMeshProUGUI activeText = usePanel ? dialogueText : narratorText;

            if (typingCoroutine != null) StopCoroutine(typingCoroutine);
            CancelAutoPlayTimer();

            if (gameObject.activeInHierarchy)
            {
                typingCoroutine = StartCoroutine(TypeText(activeText, fullText));
            }
            else
            {
                activeText.text = fullText;
                activeText.maxVisibleCharacters = 99999;
                isTyping = false;
            }

            ClearChoices();
        }

        // ═══════════ Character Image Helpers ═══════════
        private Image GetCharacterImage(CharacterPosition pos)
        {
            switch (pos)
            {
                case CharacterPosition.Left: return characterImageLeft;
                case CharacterPosition.Center: return characterImageCenter;
                case CharacterPosition.Right: return characterImageRight;
                default: return characterImageCenter;
            }
        }

        private CharacterPosition FindFreeSlot()
        {
            // Priority: Center → Left → Right (1명일 때 중앙부터)
            if (!_activeSpeakerPositions.ContainsValue(CharacterPosition.Center)) return CharacterPosition.Center;
            if (!_activeSpeakerPositions.ContainsValue(CharacterPosition.Left)) return CharacterPosition.Left;
            if (!_activeSpeakerPositions.ContainsValue(CharacterPosition.Right)) return CharacterPosition.Right;
            return CharacterPosition.Center;
        }

        private string ExtractBaseName(string spritePath)
        {
            // "Characters/카스미/기본" → "카스미"
            // "Characters/미나/검은색 버전/기본" → "미나"
            if (string.IsNullOrEmpty(spritePath)) return "";
            string[] parts = spritePath.Split('/');
            if (parts.Length >= 3 && parts[0] == "Characters") return parts[1];
            if (parts.Length >= 2) return parts[parts.Length - 2];
            return spritePath;
        }

        // ═══════════ Layout Calculation & Smooth Movement ═══════════
        private void UpdateCharacterLayout()
        {
            if (_activeSpeakerPositions.Count == 0) return;

            foreach (var pos in _activeSpeakerPositions.Values)
            {
                float targetX = 0.5f; // Default: center
                if (pos == CharacterPosition.Left) targetX = 0.25f;
                else if (pos == CharacterPosition.Center) targetX = 0.5f;
                else if (pos == CharacterPosition.Right) targetX = 0.75f;

                MoveCharacterTo(pos, targetX);
            }
        }

        private void MoveCharacterTo(CharacterPosition pos, float targetX)
        {
            int idx = (int)pos;
            Image img = GetCharacterImage(pos);
            if (img == null) return;

            if (_moveCoroutines[idx] != null)
            {
                StopCoroutine(_moveCoroutines[idx]);
            }
            
            float startX = (img.rectTransform.anchorMin.x + img.rectTransform.anchorMax.x) / 2f;
            if (Mathf.Abs(startX - targetX) < 0.005f)
            {
                SetCharacterAnchorX(img.rectTransform, targetX);
                return;
            }
            
            _moveCoroutines[idx] = StartCoroutine(SmoothMoveCharacter(img, targetX));
        }

        private IEnumerator SmoothMoveCharacter(Image target, float targetAnchorX)
        {
            RectTransform rt = target.rectTransform;
            if (rt == null) yield break;

            float startX = (rt.anchorMin.x + rt.anchorMax.x) / 2f;
            if (Mathf.Abs(startX - targetAnchorX) < 0.005f)
            {
                SetCharacterAnchorX(rt, targetAnchorX);
                yield break;
            }

            yield return null; // 1 frame wait in sync with FadeInCharacter so load frame doesn't eat move duration

            float elapsed = 0f;
            while (elapsed < MOVE_DURATION)
            {
                float dt = Mathf.Min(Time.unscaledDeltaTime, MAX_ANIM_DELTA) * (IsFastForwarding ? 10f : 1f);
                elapsed += dt;
                float t = Mathf.SmoothStep(0f, 1f, Mathf.Clamp01(elapsed / MOVE_DURATION));
                float newX = Mathf.Lerp(startX, targetAnchorX, t);
                SetCharacterAnchorX(rt, newX);
                yield return null;
            }
            SetCharacterAnchorX(rt, targetAnchorX);
        }

        private void SetCharacterAnchorX(RectTransform rt, float centerX)
        {
            // Use anchor-based positioning like old project
            // Width: 0.9 of screen (0.45 on each side of center)
            rt.anchorMin = new Vector2(centerX - 0.45f, -0.6f);
            rt.anchorMax = new Vector2(centerX + 0.45f, 0.95f);
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;
        }

        // ═══════════ Character FadeIn / FadeOut ═══════════
        private void StartFadeIn(Image img, float startAlpha = 0f)
        {
            if (img == null) return;
            if (_fadeCoroutines.ContainsKey(img) && _fadeCoroutines[img] != null) StopCoroutine(_fadeCoroutines[img]);
            _fadeCoroutines[img] = StartCoroutine(FadeInCharacter(img, startAlpha));
        }

        private IEnumerator FadeInCharacter(Image img, float startAlpha = 0f)
        {
            if (img == null) yield break;

            img.gameObject.SetActive(true);
            Color c = img.color;
            c.a = startAlpha;
            img.color = c;

            yield return null; // 1 frame wait for layout / GPU upload

            float elapsed = startAlpha * DEFAULT_FADE_SPEED;
            while (elapsed < DEFAULT_FADE_SPEED)
            {
                float dt = Mathf.Min(Time.unscaledDeltaTime, MAX_ANIM_DELTA) * (IsFastForwarding ? 10f : 1f);
                elapsed += dt;
                c = img.color; // keep dim/highlight RGB from highlight coroutine
                c.a = Mathf.SmoothStep(0f, 1f, Mathf.Clamp01(elapsed / DEFAULT_FADE_SPEED));
                img.color = c;
                yield return null;
            }
            c = img.color;
            c.a = 1f;
            img.color = c;
        }

        private void FadeOutCharacter(CharacterPosition pos)
        {
            Image img = GetCharacterImage(pos);
            if (img != null && img.gameObject.activeSelf)
            {
                if (_fadeCoroutines.ContainsKey(img) && _fadeCoroutines[img] != null) StopCoroutine(_fadeCoroutines[img]);
                _fadeCoroutines[img] = StartCoroutine(FadeOutCharacterCoroutine(img));
            }
        }

        private IEnumerator FadeOutCharacterCoroutine(Image img)
        {
            if (img == null) yield break;
            yield return null;

            Color c = ACTIVE_COLOR;
            float startAlpha = img.color.a;
            float elapsed = 0f;

            while (elapsed < DEFAULT_FADE_SPEED)
            {
                float dt = Mathf.Min(Time.unscaledDeltaTime, MAX_ANIM_DELTA) * (IsFastForwarding ? 10f : 1f);
                elapsed += dt;
                float t = Mathf.Clamp01(elapsed / DEFAULT_FADE_SPEED);
                c.a = Mathf.SmoothStep(startAlpha, 0f, t);
                img.color = c;
                yield return null;
            }

            c.a = 0f;
            img.color = c;
            img.gameObject.SetActive(false);

            // Reset for next use
            Color resetColor = ACTIVE_COLOR;
            resetColor.a = 1f;
            img.color = resetColor;
        }

        private void HideAllCharacters()
        {
            for (int s = 0; s < 3; s++) StopSlotCoroutines(s);
            DestroyGhosts();

            Image[] chars = { characterImageLeft, characterImageCenter, characterImageRight };
            foreach (var img in chars)
            {
                if (img != null)
                {
                    img.gameObject.SetActive(false);
                    img.color = ACTIVE_COLOR;
                }
            }
            _activeSpeakerPositions.Clear();
            _speakerOrder.Clear();
            _ownersBeforeNarrator.Clear();
            _xBeforeNarrator.Clear();
            _wasNarratorLinePrev = false;
        }

        // ═══════════ Speaker Highlight / Dim ═══════════
        private void UpdateSpeakerHighlight(string speaker, bool instant = false, string command = null)
        {
            if (string.IsNullOrWhiteSpace(speaker))
            {
                // If command explicitly specifies force dim or highlight, honor it
                bool forceDim = !string.IsNullOrEmpty(command) && command.Contains("FORCE_DIM");
                bool forceHighlight = !string.IsNullOrEmpty(command) && (command.Contains("FORCE_HIGHLIGHT") || command.Contains("FORCE_ACTIVE"));

                // Keep solo character bright only during black-background character intro showcases (e.g., ch0_gathering)
                bool isBlackBgShowcase = _activeSpeakerPositions.Count == 1
                                         && (_currentBgPath == "Images/bg_black" || _currentBgPath == "bg_black");
                bool keepActive = (forceHighlight || isBlackBgShowcase) && !forceDim;
                foreach (var kvp in _activeSpeakerPositions)
                {
                    DimCharacterImage(GetCharacterImage(kvp.Value), keepActive, instant);
                }
                return;
            }

            string trimmed = speaker.Trim();
            foreach (var kvp in _activeSpeakerPositions)
            {
                bool isSpeaking = kvp.Key == trimmed;
                DimCharacterImage(GetCharacterImage(kvp.Value), isSpeaking, instant);
            }
        }

        private void DimCharacterImage(Image image, bool isActive, bool instant = false)
        {
            if (image == null) return;
            if (!image.gameObject.activeSelf) return;

            Color targetColor = isActive ? ACTIVE_COLOR : DIM_COLOR;
            float duration = instant ? 0f : 0.08f;

            if (_highlightCoroutines.ContainsKey(image) && _highlightCoroutines[image] != null)
            {
                StopCoroutine(_highlightCoroutines[image]);
            }

            // Snap RGB immediately when instant, fast-forwarding, newly fading in from alpha ~0,
            // or already at target RGB (avoids 1-frame white flash on newly entering non-speakers).
            bool alreadyAtTarget =
                Mathf.Abs(image.color.r - targetColor.r) < 0.005f &&
                Mathf.Abs(image.color.g - targetColor.g) < 0.005f &&
                Mathf.Abs(image.color.b - targetColor.b) < 0.005f;

            if (duration <= 0f || image.color.a <= 0.01f || IsFastForwarding || alreadyAtTarget)
            {
                Color finalC = targetColor;
                finalC.a = image.color.a;
                image.color = finalC;
            }
            else
            {
                _highlightCoroutines[image] = StartCoroutine(FadeColorCoroutine(image, targetColor, duration));
            }
        }

        private IEnumerator FadeColorCoroutine(Image image, Color targetColor, float duration)
        {
            Color startColor = image.color;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                float dt = Mathf.Min(Time.unscaledDeltaTime, MAX_ANIM_DELTA) * (IsFastForwarding ? 10f : 1f);
                elapsed += dt;
                float smoothT = Mathf.SmoothStep(0f, 1f, Mathf.Clamp01(elapsed / duration));

                Color lerpedColor = Color.Lerp(startColor, targetColor, smoothT);
                lerpedColor.a = image.color.a; // Preserve alpha (FadeIn/FadeOut controls alpha)
                image.color = lerpedColor;
                yield return null;
            }

            Color finalC = targetColor;
            finalC.a = image.color.a;
            image.color = finalC;
        }

        // ═══════════ Sprite Loading ═══════════
        private static Dictionary<string, Sprite> _spriteCache = new Dictionary<string, Sprite>();

        private IEnumerator PreloadChapterSpritesRoutine(DialogueContainer container)
        {
            if (container == null || container.nodes == null) yield break;

            List<string> toLoad = new List<string>();
            HashSet<string> seen = new HashSet<string>();

            foreach (var n in container.nodes)
            {
                if (n == null) continue;
                AddPreloadPath(n.backgroundSprite, seen, toLoad);
                AddPreloadPath(n.characterSpriteLeft, seen, toLoad);
                AddPreloadPath(n.characterSpriteCenter, seen, toLoad);
                AddPreloadPath(n.characterSpriteRight, seen, toLoad);
                AddPreloadPath(n.characterSprite, seen, toLoad);
            }

            // Wait 1 frame for the initial node display to settle, then warm up 1 uncached sprite per frame
            yield return null;
            for (int i = 0; i < toLoad.Count; i++)
            {
                string path = toLoad[i];
                if (_spriteCache.TryGetValue(path, out Sprite cached) && cached != null) continue;
                LoadSpriteCached(path);
                yield return null;
            }
            _preloadCoroutine = null;
        }

        private static void AddPreloadPath(string path, HashSet<string> seen, List<string> toLoad)
        {
            if (string.IsNullOrEmpty(path)) return;
            if (_spriteCache.TryGetValue(path, out Sprite cached) && cached != null) return;
            if (seen.Add(path)) toLoad.Add(path);
        }

        private void LoadSpriteToImage(Image img, string spritePath)
        {
            if (img == null || string.IsNullOrEmpty(spritePath)) return;

            Sprite sprite = LoadSpriteCached(spritePath);
            if (sprite == null)
            {
                // Missing expression → fall back to the same character's default sprite instead of
                // leaving the slot's previous sprite (which may belong to a different character).
                string fallback = null;
                int slash = spritePath.LastIndexOf('/');
                if (slash > 0) fallback = spritePath.Substring(0, slash) + "/기본";
                if (fallback != null && fallback != spritePath) sprite = LoadSpriteCached(fallback);
                Debug.LogWarning($"[DialogueUI] Missing character sprite '{spritePath}'" + (sprite != null ? $", using '{fallback}'" : ""));
            }

            if (sprite != null)
            {
                img.sprite = sprite;
                img.preserveAspect = true;
                img.rectTransform.offsetMin = Vector2.zero;
                img.rectTransform.offsetMax = Vector2.zero;
                img.enabled = true;
            }
        }

        public static Sprite LoadSpriteCached(string spritePath)
        {
            if (string.IsNullOrEmpty(spritePath)) return null;
            if (_spriteCache.TryGetValue(spritePath, out Sprite cachedSprite) && cachedSprite != null)
                return cachedSprite;

            Sprite sprite = Resources.Load<Sprite>(spritePath);

            if (sprite == null)
            {
                Sprite[] allSprites = Resources.LoadAll<Sprite>(spritePath);
                if (allSprites != null && allSprites.Length > 0) sprite = allSprites[0];
            }

            if (sprite == null)
            {
                Texture2D tex = Resources.Load<Texture2D>(spritePath);
                if (tex != null)
                {
                    sprite = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), new Vector2(0.5f, 0.5f));
                }
            }

            if (sprite != null) _spriteCache[spritePath] = sprite;
            return sprite;
        }

        // ═══════════ Background ═══════════
        private string _currentBgPath;

        private System.Collections.IEnumerator CrossfadePanels(bool toDialogue)
        {
            GameObject narratorParent = narratorText != null ? narratorText.transform.parent.gameObject : null;
            if (dialoguePanel == null || narratorParent == null) yield break;

            CanvasGroup diagCG = dialoguePanel.GetComponent<CanvasGroup>();
            if (diagCG == null) diagCG = dialoguePanel.AddComponent<CanvasGroup>();

            CanvasGroup narrCG = narratorParent.GetComponent<CanvasGroup>();
            if (narrCG == null) narrCG = narratorParent.AddComponent<CanvasGroup>();

            float duration = 0.4f;
            float elapsed = 0f;

            float startDiagAlpha = diagCG.alpha;
            float startNarrAlpha = narrCG.alpha;

            if (toDialogue)
            {
                dialoguePanel.SetActive(true);
                while (elapsed < duration)
                {
                    elapsed += Time.deltaTime * (IsFastForwarding ? 10f : 1f);
                    float t = elapsed / duration;
                    diagCG.alpha = Mathf.SmoothStep(startDiagAlpha, 1f, t);
                    narrCG.alpha = Mathf.SmoothStep(startNarrAlpha, 0f, t);
                    yield return null;
                }
                diagCG.alpha = 1f;
                narrCG.alpha = 0f;
                narratorParent.SetActive(false);
            }
            else
            {
                narratorParent.SetActive(true);
                while (elapsed < duration)
                {
                    elapsed += Time.deltaTime * (IsFastForwarding ? 10f : 1f);
                    float t = elapsed / duration;
                    narrCG.alpha = Mathf.SmoothStep(startNarrAlpha, 1f, t);
                    diagCG.alpha = Mathf.SmoothStep(startDiagAlpha, 0f, t);
                    yield return null;
                }
                narrCG.alpha = 1f;
                diagCG.alpha = 0f;
                dialoguePanel.SetActive(false);
            }
        }

        public void UpdateBackground(string spritePath)
        {
            if (backgroundImage == null) return;
            if (string.IsNullOrEmpty(spritePath)) return; // empty = keep previous background
            if (spritePath == _currentBgPath && backgroundImage.enabled && backgroundImage.sprite != null) return;

            Sprite sprite = LoadSpriteCached(spritePath);
            if (sprite != null)
            {
                backgroundImage.sprite = sprite;
                backgroundImage.color = Color.white; // Ensure alpha is 1
                backgroundImage.enabled = true;
                _currentBgPath = spritePath;
            }
        }

        // ═══════════ Typing ═══════════
        private IEnumerator TypeText(TextMeshProUGUI target, string text)
        {
            Debug.Log($"[DialogueUI] TypeText started for: {text}");
            isTyping = true;
            
            if (target != null)
            {
                target.text = text;
                target.maxVisibleCharacters = 0; // 플리커링 방지를 위해 미리 0으로 설정
            }

            // Canvas Layout이 반영될 수 있도록 1프레임 대기
            yield return null;
            // 배경 전환(암전) 중에는 화면이 다시 밝아진 뒤부터 타이핑 시작
            while (_isTransitioningScene) yield return null;

            if (target != null)
            {
                target.ForceMeshUpdate(true);
                
                // === 내레이션 텍스트 세로 밀림 현상 방지 ===
                if (target == narratorText)
                {
                    float prefH = target.preferredHeight;
                    target.rectTransform.anchorMin = new Vector2(0f, 0.5f);
                    target.rectTransform.anchorMax = new Vector2(1f, 0.5f);
                    target.rectTransform.sizeDelta = new Vector2(0, prefH);
                    target.rectTransform.anchoredPosition = Vector2.zero;
                    target.alignment = TextAlignmentOptions.Top;
                }

                target.maxVisibleCharacters = 0; // 혹시 몰라 다시 0으로 설정
                Debug.Log($"[DialogueUI] TMPro rect size: {target.rectTransform.rect.size}, Active: {target.gameObject.activeInHierarchy}");
            }

            int totalVisibleChars = target != null ? target.textInfo.characterCount : 0;
            if (totalVisibleChars == 0 && !string.IsNullOrEmpty(text))
            {
                totalVisibleChars = text.Length; // Failsafe if TMPro returns 0 incorrectly
            }
            int visibleCount = 0;
            Debug.Log($"[DialogueUI] Total visible chars: {totalVisibleChars}");

            float nextCharTime = Time.unscaledTime;
            while (visibleCount <= totalVisibleChars && target != null)
            {
                while (IsModalOpen() || isUiHidden)
                {
                    yield return null;
                    nextCharTime = Time.unscaledTime;
                }
                if (target == null) break;

                target.maxVisibleCharacters = visibleCount;
                
                if (visibleCount > 0 && visibleCount <= target.textInfo.characterCount)
                {
                    char c = target.textInfo.characterInfo[visibleCount - 1].character;
                    if (c == '\n')
                    {
                        yield return _cachedNewlineDelay;
                        nextCharTime = Time.unscaledTime;
                    }
                }
                
                visibleCount++;
                
                nextCharTime += SettingsData.TextSpeed;
                while (Time.unscaledTime < nextCharTime)
                {
                    if (IsModalOpen() || isUiHidden)
                    {
                        float remaining = Mathf.Max(0f, nextCharTime - Time.unscaledTime);
                        while (IsModalOpen() || isUiHidden)
                        {
                            yield return null;
                        }
                        nextCharTime = Time.unscaledTime + remaining;
                    }
                    yield return null;
                }
            }
            isTyping = false;
            _typingEndTime = Time.unscaledTime;
            Debug.Log($"[DialogueUI] TypeText finished.");

            if (isAutoPlay)
            {
                autoPlayCoroutine = StartCoroutine(AutoAdvanceAfterDelay());
            }
        }

        private IEnumerator AutoAdvanceAfterDelay()
        {
            float elapsed = 0f;
            while (elapsed < SettingsData.AutoPlayDelay)
            {
                if (!isAutoPlay) yield break;
                if (!_isTransitioningScene && !IsModalOpen() && !isUiHidden)
                {
                    elapsed += Time.unscaledDeltaTime;
                }
                yield return null;
            }
            while (_isTransitioningScene || IsModalOpen() || isUiHidden)
            {
                if (!isAutoPlay) yield break;
                yield return null;
            }
            if (isAutoPlay && DialogueManager.Instance != null)
            {
                DialogueManager.Instance.AdvanceDialogue();
            }
        }

        private LanguageUI _cachedLanguageUI;
        private ExtraUI _cachedExtraUI;

        private bool IsModalOpen()
        {
            if (_cachedBacklogUI == null) _cachedBacklogUI = Object.FindFirstObjectByType<BacklogUI>(UnityEngine.FindObjectsInactive.Include);
            if (_cachedSettingsUI == null) _cachedSettingsUI = Object.FindFirstObjectByType<SettingsUI>(UnityEngine.FindObjectsInactive.Include);
            if (_cachedLanguageUI == null) _cachedLanguageUI = Object.FindFirstObjectByType<LanguageUI>(UnityEngine.FindObjectsInactive.Include);
            if (_cachedExtraUI == null) _cachedExtraUI = Object.FindFirstObjectByType<ExtraUI>(UnityEngine.FindObjectsInactive.Include);
            
            if (_cachedBacklogUI != null && _cachedBacklogUI.IsOpen) return true;
            if (_cachedSettingsUI != null && _cachedSettingsUI.gameObject.activeInHierarchy) return true;
            if (_cachedLanguageUI != null && _cachedLanguageUI.gameObject.activeInHierarchy) return true;
            if (_cachedExtraUI != null && _cachedExtraUI.gameObject.activeInHierarchy) return true;

            return false;
        }

        // ═══════════ Click / Input ═══════════
        public void SkipTyping()
        {
            Debug.Log($"[DialogueUI] SkipTyping called.");
            if (typingCoroutine != null) StopCoroutine(typingCoroutine);
            if (dialogueText != null) dialogueText.maxVisibleCharacters = 99999;
            if (narratorText != null) narratorText.maxVisibleCharacters = 99999;
            isTyping = false;
            _typingEndTime = 0f; // Allow immediate next click when manually skipped

            CancelAutoPlayTimer();
            if (isAutoPlay)
            {
                autoPlayCoroutine = StartCoroutine(AutoAdvanceAfterDelay());
            }
        }

        
        private bool isUiHidden = false;
        private int _lastUiUnhideFrame = -1;
        private bool _currentlyInDialoguePanel = true;

        public bool IsUiHidden => isUiHidden;

        public void SetUiHidden(bool hidden)
        {
            if (isUiHidden && !hidden)
            {
                _lastUiUnhideFrame = Time.frameCount;
            }
            isUiHidden = hidden;
            if (isUiHidden) StopAutoPlay();

            GameObject narratorParent = narratorText != null ? narratorText.transform.parent.gameObject : null;
            if (_currentlyInDialoguePanel)
            {
                if (dialoguePanel != null) dialoguePanel.SetActive(!isUiHidden);
            }
            else
            {
                if (narratorParent != null) narratorParent.SetActive(!isUiHidden);
            }

            if (autoButton != null) autoButton.gameObject.SetActive(!isUiHidden && _currentlyInDialoguePanel);
            if (backlogButton != null) backlogButton.gameObject.SetActive(!isUiHidden && _currentlyInDialoguePanel);
            if (isUiHidden)
            {
                if (skipIndicator != null) skipIndicator.SetActive(false);
                if (nextIndicator != null) nextIndicator.SetActive(false);
                if (narratorNextIndicator != null) narratorNextIndicator.SetActive(false);
            }
        }

        public void RestoreHiddenUI() => SetUiHidden(false);

        private void Update()
        {
            if (GameManager.Instance != null && GameManager.Instance.CurrentPhase != GamePhase.Dialogue)
            {
                _spaceHoldTimer = 0f;
                if (skipIndicator != null && skipIndicator.activeSelf) skipIndicator.SetActive(false);
                return;
            }
            if (IsModalOpen())
            {
                _spaceHoldTimer = 0f;
                if (skipIndicator != null && skipIndicator.activeSelf) skipIndicator.SetActive(false);
                return;
            }

            if (HalloweenVN.Core.SettingsData.IsSkipKeyPressed())
                _spaceHoldTimer += Time.unscaledDeltaTime;
            else
                _spaceHoldTimer = 0f;

            bool isChoiceActive = choicePanel != null && choicePanel.activeSelf;
            bool isPlaying = DialogueManager.Instance != null && DialogueManager.Instance.IsPlaying;
            bool showNext = isPlaying && !isTyping && !isUiHidden && !_isTransitioningScene && !isChoiceActive && !string.IsNullOrEmpty(fullText);

            if (nextIndicator != null)
            {
                bool active = showNext && _currentlyInDialoguePanel;
                if (nextIndicator.activeSelf != active) nextIndicator.SetActive(active);
                if (active)
                {
                    RectTransform rt = nextIndicator.transform as RectTransform;
                    if (rt != null) rt.anchoredPosition = new Vector2(-36f, 20f + Mathf.Sin(Time.unscaledTime * 5f) * 3f);
                }
            }
            if (narratorNextIndicator != null)
            {
                bool active = showNext && !_currentlyInDialoguePanel;
                if (narratorNextIndicator.activeSelf != active) narratorNextIndicator.SetActive(active);
                if (active)
                {
                    RectTransform rt = narratorNextIndicator.transform as RectTransform;
                    if (rt != null) rt.anchoredPosition = new Vector2(-90f, 80f + Mathf.Sin(Time.unscaledTime * 5f) * 3f);
                }
            }

            // Mouse wheel up or Backlog key / PageUp key to open log (Allow this even during choices)
            bool openLogKey = HalloweenVN.Core.SettingsData.WasBacklogKeyPressedThisFrame();
            if ((UnityEngine.InputSystem.Mouse.current != null && UnityEngine.InputSystem.Mouse.current.scroll.ReadValue().y > 0) || openLogKey)
            {
                if (_cachedBacklogUI == null)
                {
                    _cachedBacklogUI = Object.FindFirstObjectByType<BacklogUI>(UnityEngine.FindObjectsInactive.Include);
                }
                if (_cachedBacklogUI != null && !_cachedBacklogUI.IsOpen)
                {
                    if (isUiHidden) SetUiHidden(false);
                    if (openLogKey && HalloweenVN.Core.AudioManager.Instance != null)
                        HalloweenVN.Core.AudioManager.Instance.PlaySFX("sfx_ui_click");
                    _cachedBacklogUI.ShowBacklog();
                    return; // Stop processing further input for this frame
                }
            }

            if (isChoiceActive)
            {
                if (skipIndicator != null && skipIndicator.activeSelf) skipIndicator.SetActive(false);
                return;
            }

            // 1. Right click or Hide UI key to toggle UI visibility (to see CG/Backgrounds)
            if ((Mouse.current != null && Mouse.current.rightButton.wasPressedThisFrame) ||
                HalloweenVN.Core.SettingsData.WasHideUiKeyPressedThisFrame())
            {
                SetUiHidden(!isUiHidden);
                return;
            }

            // If UI is hidden, left clicking or Advance/Enter key restores it instead of advancing text
            if (isUiHidden)
            {
                if ((Mouse.current != null && Mouse.current.leftButton.wasPressedThisFrame) ||
                    HalloweenVN.Core.SettingsData.WasAdvanceKeyPressedThisFrame())
                {
                    SetUiHidden(false);
                }
                return;
            }

            // Auto-Play key to toggle Auto-Play
            if (HalloweenVN.Core.SettingsData.WasAutoKeyPressedThisFrame() && isPlaying && !_isTransitioningScene)
            {
                if (HalloweenVN.Core.AudioManager.Instance != null)
                    HalloweenVN.Core.AudioManager.Instance.PlaySFX("sfx_ui_click");
                ToggleAutoPlay();
                return;
            }

            // 2. Skip Logic
            bool isSkipPressed = IsFastForwarding;
            bool showSkip = isSkipPressed && isPlaying && !isChoiceActive;
            if (skipIndicator != null && skipIndicator.activeSelf != showSkip)
            {
                skipIndicator.SetActive(showSkip);
            }

            if (isSkipPressed)
            {
                if (isPlaying && !isChoiceActive)
                {
                    if (isTyping) SkipTyping();
                    
                    ctrlSkipTimer += Time.deltaTime;
                    if (ctrlSkipTimer >= 0.05f)
                    {
                        ctrlSkipTimer = 0f;
                        if (!isTyping && !_isTransitioningScene) DialogueManager.Instance.AdvanceDialogue();
                    }
                }
            }
            else
            {
                ctrlSkipTimer = 0f;
            }

            // 3. Advance key / Enter to advance dialogue
            if (HalloweenVN.Core.SettingsData.WasAdvanceKeyPressedThisFrame())
            {
                OnClick();
            }
        }


        private float _lastClickTime = 0f;
        private float _typingEndTime = -1f;

        public void OnClick() { 
            if (IsModalOpen()) return;
            if (_isTransitioningScene) return; // Prevent double-trigger from UI Event System + Input System
            if (isUiHidden)
            {
                SetUiHidden(false);
                return;
            }
            if (Time.frameCount == _lastUiUnhideFrame) return;
            
            // 1. Prevent physical double-trigger from Unity Input System (0.05s)
            if (Time.unscaledTime - _lastClickTime < 0.05f) return; 

            // 2. Prevent accidental advance right after text finishes typing (0.1s)
            if (!isTyping && Time.unscaledTime - _typingEndTime < 0.1f) 
            {
                return; // Do NOT update _lastClickTime here, so the player isn't penalized for mashing!
            }

            // Only update last click time when the click is actually accepted!
            _lastClickTime = Time.unscaledTime;
            CancelAutoPlayTimer();

            if (HalloweenVN.Core.AudioManager.Instance != null)
            {
                HalloweenVN.Core.AudioManager.Instance.PlaySFX("sfx_ui_click");
            }

            Debug.Log($"[DialogueUI] OnClick triggered. isTyping={isTyping}");
            if (isTyping)
            {
                SkipTyping();
            }
            else
            {
                if (DialogueManager.Instance != null)
                {
                    DialogueManager.Instance.AdvanceDialogue();
                }
            }
        }

        // ═══════════ Choices ═══════════
        public void ShowChoices(List<DialogueChoice> choices)
        {
            ClearChoices();
            if (choicePanel != null) choicePanel.SetActive(true);

            for (int i = 0; i < choices.Count; i++)
            {
                int index = i;
                GameObject btnObj = Instantiate(choiceButtonPrefab, choiceButtonContainer);
                btnObj.AddComponent<UIHoverSound>();
                btnObj.SetActive(true);

                TextMeshProUGUI btnText = btnObj.GetComponentInChildren<TextMeshProUGUI>();
                if (btnText != null) {
                    var dm = DialogueManager.Instance;
                    btnText.text = HalloweenVN.Core.Loc.ChoiceText(dm?.CurrentDialogueId, dm?.CurrentNode != null ? dm.CurrentNode.id : -1, i, choices[i]);
                }

                Button btn = btnObj.GetComponent<Button>();
                if (btn != null)
                {
                    btn.onClick.AddListener(() => { ClearChoices();
                        if (DialogueManager.Instance != null)
                        {
                            DialogueManager.Instance.SelectChoice(index);
                        }
                    });
                }
            }
        }

        private void ClearChoices()
        {
            if (choicePanel != null) choicePanel.SetActive(false);
            if (choiceButtonContainer != null)
            {
                foreach (Transform child in choiceButtonContainer)
                {
                    Destroy(child.gameObject);
                }
            }
        }

        // ═══════════ Auto / Skip ═══════════
        public void ToggleAutoPlay()
        {
            isAutoPlay = !isAutoPlay;
            if (autoButtonText != null)
            {
                UpdateLanguage();
            }

            CancelAutoPlayTimer();
            if (isAutoPlay && !isTyping && DialogueManager.Instance != null && DialogueManager.Instance.IsPlaying)
            {
                autoPlayCoroutine = StartCoroutine(AutoAdvanceAfterDelay());
            }
        }

        private void CancelAutoPlayTimer()
        {
            if (autoPlayCoroutine != null)
            {
                StopCoroutine(autoPlayCoroutine);
                autoPlayCoroutine = null;
            }
        }
        
        private void StopAutoPlay()
        {
            isAutoPlay = false;
            if (autoButtonText != null) UpdateLanguage();
            CancelAutoPlayTimer();
        }

        public void ApplyOpacity(float opacity)
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
    }
}










