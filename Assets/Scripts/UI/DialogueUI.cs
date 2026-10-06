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
// ═══════════ Typing & Auto ═══════════
        private BacklogUI _cachedBacklogUI;
        private SettingsUI _cachedSettingsUI;
        private WaitForSeconds _cachedNewlineDelay = new WaitForSeconds(0.15f);
        private WaitForSeconds _cachedTextDelay;
        private float _lastTextSpeed = -1f;

        private Coroutine typingCoroutine;
        private Coroutine autoPlayCoroutine;
        private bool isTyping;

        private bool IsFastForwarding
        {
            get
            {
                if (UnityEngine.InputSystem.Keyboard.current == null) return false;
                if (HalloweenVN.Core.SettingsData.SkipKey == HalloweenVN.Core.SettingsData.SkipKeyOption.Ctrl)
                    return UnityEngine.InputSystem.Keyboard.current.leftCtrlKey.isPressed || UnityEngine.InputSystem.Keyboard.current.rightCtrlKey.isPressed;
                if (HalloweenVN.Core.SettingsData.SkipKey == HalloweenVN.Core.SettingsData.SkipKeyOption.Shift)
                    return UnityEngine.InputSystem.Keyboard.current.leftShiftKey.isPressed || UnityEngine.InputSystem.Keyboard.current.rightShiftKey.isPressed;
                if (HalloweenVN.Core.SettingsData.SkipKey == HalloweenVN.Core.SettingsData.SkipKeyOption.Space)
                    return UnityEngine.InputSystem.Keyboard.current.spaceKey.isPressed;
                return false;
            }
        }

        private bool isAutoPlay;
        private float ctrlSkipTimer = 0f;
        private string fullText;

        // ═══════════ Character Position System (ported from old project) ═══════════
        private static readonly Color DIM_COLOR = new Color(0.3f, 0.3f, 0.3f, 1f);
        private static readonly Color ACTIVE_COLOR = Color.white;
        private const float DEFAULT_FADE_SPEED = 0.08f;
        private const float MOVE_DURATION = 0.25f;

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
            
            RectTransform rt = narratorObj.AddComponent<RectTransform>();
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;

            Image img = narratorObj.AddComponent<Image>();
            img.color = new Color(0, 0, 0, 1f); // Solid black background for monologue

            Button btn = narratorObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.None;
            btn.onClick.AddListener(OnClick);

            // Child: text label (separate GameObject to avoid Graphic conflict)
            GameObject textObj = new GameObject("NarratorLabel");
            textObj.layer = LayerMask.NameToLayer("UI");
            textObj.transform.SetParent(narratorObj.transform, false);

            RectTransform textRt = textObj.AddComponent<RectTransform>();
            textRt.anchorMin = Vector2.zero;
            textRt.anchorMax = Vector2.one;
            textRt.offsetMin = Vector2.zero;
            textRt.offsetMax = Vector2.zero;
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
            if (autoButtonText != null) autoButtonText.fontSize = btnSize;            // Adjust dialogue and speaker TMP text sizes
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
            if (dialoguePanel != null)
                dialoguePanel.SetActive(true);
            ClearChoices();
            // NOTE: character tracking is NOT cleared here. Clearing it while sprites were still
            // visible left "orphan" characters on screen that no node could remove.
            // HideDialoguePanel (on dialogue end) hides and clears everything instead.
            _freshDialogue = true;
        }

        public void HideDialoguePanel()
        {
            if (dialoguePanel != null)
                dialoguePanel.SetActive(false);
            ClearChoices();
            StopAutoPlay();
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

        
        // Ghost copies used to fade out characters that leave while their slot image is reused
        private readonly List<GameObject> _ghostImages = new List<GameObject>();

        // Last layout target assigned to each slot (-1 = empty). Used to detect interrupted slides.
        private readonly float[] _lastTargetX = { -1f, -1f, -1f };

        public void UpdateVisualsOnly(DialogueNode node, bool instant)
        {
            bool wasNarrator = !_currentlyInDialoguePanel;
            bool isNarratorNow = string.IsNullOrEmpty(node.speaker);
            bool usePanelNow = !isNarratorNow;

            if (wasNarrator && usePanelNow)
            {
                instant = true;
            }

            Image[] imgs = { characterImageLeft, characterImageCenter, characterImageRight };
            bool immediate = instant || node.noFade;

            // 1. Requested sprites per slot (legacy single-sprite → center)
            string[] requested = { node.characterSpriteLeft, node.characterSpriteCenter, node.characterSpriteRight };
            if (!string.IsNullOrEmpty(node.characterSprite))
            {
                requested[0] = null; requested[1] = node.characterSprite; requested[2] = null;
            }

            // 2. New owner per slot (same character listed twice → keep the first slot only)
            string[] newOwner = new string[3];
            HashSet<string> newNames = new HashSet<string>();
            for (int s = 0; s < 3; s++)
            {
                if (string.IsNullOrEmpty(requested[s])) continue;
                string name = ExtractBaseName(requested[s]);
                if (newNames.Contains(name)) { requested[s] = null; continue; }
                newOwner[s] = name;
                newNames.Add(name);
            }

            // 3. Snapshot the previous on-screen state BEFORE touching any image.
            //    A character only counts as "on screen" if its slot image is actually active
            //    (fixes characters never re-appearing after HideAllCharacters left stale tracking).
            string[] prevOwner = new string[3];
            Dictionary<string, int> prevSlotOf = new Dictionary<string, int>();
            foreach (var kvp in _activeSpeakerPositions)
            {
                int s = (int)kvp.Value;
                Image img = imgs[s];
                if (img == null || !img.gameObject.activeSelf) continue;
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

                // Previous occupant leaves the screen entirely → fade out a ghost copy
                if (old != null && old != name && !newNames.Contains(old))
                {
                    if (!immediate) SpawnGhostFadeOut(img);
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
                        
                        // Interrupted mid-slide (e.g. fast-clicking during an entrance): snap so it
                        // doesn't keep drifting. Settled characters glide normally via MoveCharacterTo.
                        if (wasMidSlide) SetCharacterAnchorX(img.rectTransform, targetX[s]);
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
                    if (!immediate && (node.slideIn || node.slideFromRight || anyoneStaying))
                    {
                        if (node.slideFromRight) startX = 1.5f;
                        else startX = targetX[s] > 0.5f ? 1.5f : -0.5f;
                    }
                    SetCharacterAnchorX(img.rectTransform, startX);

                    if (immediate)
                    {
                        img.gameObject.SetActive(true);
                        ForceOpaque(img);
                    }
                    else
                    {
                        StartFadeIn(img);
                        if (Mathf.Abs(startX - targetX[s]) > 0.01f) MoveCharacterTo((CharacterPosition)s, targetX[s]);
                    }
                }
            }

            for (int s = 0; s < 3; s++) _lastTargetX[s] = newOwner[s] != null ? targetX[s] : -1f;

            // Dim/Highlight based on speaker
            bool instantHighlight = instant || (wasNarrator && usePanelNow);
            UpdateSpeakerHighlight(node.speaker, instantHighlight);
            UpdateBackground(node.backgroundSprite);
        }

        /// <summary>
        /// Screen X (anchor center) per slot. Positions depend only on how many characters are shown
        /// and their left-to-right slot order: 1 → 50%, 2 → 25/75%, 3 → 20/50/80%.
        /// </summary>
        private static float[] ComputeLayoutTargets(string[] owner)
        {
            float[] result = { 0.25f, 0.5f, 0.75f };
            List<int> used = new List<int>();
            for (int s = 0; s < 3; s++) if (owner[s] != null) used.Add(s);
            float[] xs;
            if (used.Count == 1) xs = new[] { 0.5f };
            else if (used.Count == 2) xs = new[] { 0.25f, 0.75f };
            else xs = new[] { 0.20f, 0.50f, 0.80f };
            
            for (int i = 0; i < used.Count; i++)
            {
                int s = used[i];
                float target = xs[i];
                
                // Character specific visual offsets to account for sprite widths
                if (owner[s] == "리나") // 850px (narrow)
                {
                    if (target < 0.5f) target += 0.05f;
                    else if (target > 0.5f) target -= 0.05f;
                }
                
                result[s] = target;
            }
            return result;
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

        private void SpawnGhostFadeOut(Image source)
        {
            if (source == null || !source.gameObject.activeSelf || source.sprite == null) return;
            GameObject ghost = Instantiate(source.gameObject, source.transform.parent);
            ghost.name = source.gameObject.name + "_Ghost";
            ghost.transform.SetSiblingIndex(source.transform.GetSiblingIndex());
            Image gImg = ghost.GetComponent<Image>();
            if (gImg == null) { Destroy(ghost); return; }
            gImg.raycastTarget = false;
            _ghostImages.Add(ghost);
            StartCoroutine(GhostFadeOutRoutine(ghost, gImg));
        }

        private IEnumerator GhostFadeOutRoutine(GameObject ghost, Image img)
        {
            Color c = img.color;
            float startAlpha = c.a;
            float elapsed = 0f;
            while (elapsed < DEFAULT_FADE_SPEED && ghost != null)
            {
                elapsed += Time.deltaTime * (IsFastForwarding ? 10f : 1f);
                c.a = Mathf.Lerp(startAlpha, 0f, Mathf.SmoothStep(0f, 1f, elapsed / DEFAULT_FADE_SPEED));
                img.color = c;
                yield return null;
            }
            _ghostImages.Remove(ghost);
            if (ghost != null) Destroy(ghost);
        }

        private void DestroyGhosts()
        {
            foreach (var g in _ghostImages) if (g != null) Destroy(g);
            _ghostImages.Clear();
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
            if (dialoguePanel != null) dialoguePanel.SetActive(usePanel);
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
            if (string.IsNullOrEmpty(spritePath)) return "";
            string[] parts = spritePath.Split('/');
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
            if (Mathf.Abs(startX - targetX) < 0.01f)
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
            if (Mathf.Abs(startX - targetAnchorX) < 0.01f)
            {
                SetCharacterAnchorX(rt, targetAnchorX);
                yield break;
            }

            float elapsed = 0f;
            while (elapsed < MOVE_DURATION)
            {
                elapsed += Time.deltaTime * (IsFastForwarding ? 10f : 1f);
                float t = Mathf.SmoothStep(0f, 1f, elapsed / MOVE_DURATION);
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

            yield return null; // 1 frame wait for layout

            float elapsed = startAlpha * DEFAULT_FADE_SPEED;
            while (elapsed < DEFAULT_FADE_SPEED)
            {
                elapsed += Time.deltaTime * (IsFastForwarding ? 10f : 1f);
                c = img.color; // keep dim/highlight RGB from highlight coroutine
                c.a = Mathf.SmoothStep(0f, 1f, elapsed / DEFAULT_FADE_SPEED);
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
                elapsed += Time.deltaTime * (IsFastForwarding ? 10f : 1f);
                float t = elapsed / DEFAULT_FADE_SPEED;
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
        }

        // ═══════════ Speaker Highlight / Dim ═══════════
        private void UpdateSpeakerHighlight(string speaker, bool instant = false)
        {
            if (string.IsNullOrWhiteSpace(speaker))
            {
                // Narrator — all active characters stay bright
                foreach (var kvp in _activeSpeakerPositions)
                {
                    DimCharacterImage(GetCharacterImage(kvp.Value), true, instant);
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
            
            if (duration <= 0f)
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
            yield return null; // 1 frame buffer
            Color startColor = image.color;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                elapsed += Time.deltaTime * (IsFastForwarding ? 10f : 1f);
                float smoothT = Mathf.SmoothStep(0f, 1f, elapsed / duration);

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
                img.SetNativeSize();
                img.enabled = true;
            }
        }

        private static Sprite LoadSpriteCached(string spritePath)
        {
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

            while (visibleCount <= totalVisibleChars && target != null)
            {
                target.maxVisibleCharacters = visibleCount;
                
                // 줄바꿈(\n) 문자가 출력되었을 때 0.7초 대기 (유저 요청)
                if (visibleCount > 0 && visibleCount <= target.textInfo.characterCount)
                {
                    char c = target.textInfo.characterInfo[visibleCount - 1].character;
                    if (c == '\n')
                    {
                        yield return _cachedNewlineDelay;
                    }
                }
                
                visibleCount++;
                if (_lastTextSpeed != SettingsData.TextSpeed)
                {
                    _lastTextSpeed = SettingsData.TextSpeed;
                    _cachedTextDelay = new WaitForSeconds(_lastTextSpeed);
                }
                yield return _cachedTextDelay;
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
            yield return new WaitForSeconds(SettingsData.AutoPlayDelay);
            while (_isTransitioningScene || IsModalOpen()) yield return null;
            if (isAutoPlay && DialogueManager.Instance != null)
            {
                DialogueManager.Instance.AdvanceDialogue();
            }
        }

        private bool IsModalOpen()
        {
            if (_cachedBacklogUI == null) _cachedBacklogUI = Object.FindFirstObjectByType<BacklogUI>(UnityEngine.FindObjectsInactive.Include);
            if (_cachedSettingsUI == null) _cachedSettingsUI = Object.FindFirstObjectByType<SettingsUI>(UnityEngine.FindObjectsInactive.Include);
            
            if (_cachedBacklogUI != null && _cachedBacklogUI.IsOpen) return true;
            if (_cachedSettingsUI != null && _cachedSettingsUI.gameObject.activeInHierarchy) return true;

            var langUi = Object.FindFirstObjectByType<LanguageUI>(UnityEngine.FindObjectsInactive.Include);
            if (langUi != null && langUi.gameObject.activeInHierarchy) return true;

            var extraUi = Object.FindFirstObjectByType<ExtraUI>(UnityEngine.FindObjectsInactive.Include);
            if (extraUi != null && extraUi.gameObject.activeInHierarchy) return true;

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
            _typingEndTime = Time.unscaledTime;

            CancelAutoPlayTimer();
            if (isAutoPlay)
            {
                autoPlayCoroutine = StartCoroutine(AutoAdvanceAfterDelay());
            }
        }

        
        private bool isUiHidden = false;
        private bool _currentlyInDialoguePanel = true;
        

        private void Update()
        {
            if (GameManager.Instance != null && GameManager.Instance.CurrentPhase != GamePhase.Dialogue) return;
            if (choicePanel != null && choicePanel.activeSelf) return;
            if (IsModalOpen()) return;

            // 1. Right click to toggle UI visibility (to see CG/Backgrounds)
            if (Mouse.current != null && Mouse.current.rightButton.wasPressedThisFrame)
            {
                isUiHidden = !isUiHidden;
                if (isUiHidden) StopAutoPlay();
                if (dialoguePanel != null) dialoguePanel.SetActive(!isUiHidden);
                if (autoButton != null) autoButton.gameObject.SetActive(!isUiHidden);
                if (backlogButton != null) backlogButton.gameObject.SetActive(!isUiHidden);
            }

            // If UI is hidden, left clicking restores it instead of advancing text
            if (isUiHidden)
            {
                if ((Mouse.current != null && Mouse.current.leftButton.wasPressedThisFrame) || (Keyboard.current != null && Keyboard.current.spaceKey.wasPressedThisFrame) || (Keyboard.current != null && Keyboard.current.enterKey.wasPressedThisFrame))
                {
                    isUiHidden = false;
                    if (dialoguePanel != null) dialoguePanel.SetActive(true);
                    if (autoButton != null) autoButton.gameObject.SetActive(true);
                    if (backlogButton != null) backlogButton.gameObject.SetActive(true);
                }
                return;
            }

            
            // 3. Ctrl Skip Logic
            bool isSkipPressed = IsFastForwarding;

            if (isSkipPressed)
            {
                if (DialogueManager.Instance != null && DialogueManager.Instance.IsPlaying && (choicePanel == null || !choicePanel.activeSelf))
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

            // 2. Mouse Scroll Up to open Backlog
            if (Mouse.current != null && Mouse.current.scroll.ReadValue().y > 0)
            {
                if (_cachedBacklogUI == null)
                {
                    _cachedBacklogUI = Object.FindFirstObjectByType<BacklogUI>(UnityEngine.FindObjectsInactive.Include);
                }

                if (_cachedBacklogUI != null && !_cachedBacklogUI.IsOpen)
                {
                    _cachedBacklogUI.ShowBacklog();
                }
            }

            // 3. Space / Enter to advance dialogue
            if ((Keyboard.current != null && Keyboard.current.spaceKey.wasPressedThisFrame) || (Keyboard.current != null && Keyboard.current.enterKey.wasPressedThisFrame))
            {
                OnClick();
            }
        }


        private float _lastClickTime = 0f;
        private float _typingEndTime = -1f;

        public void OnClick() { 
            if (IsModalOpen()) return;
            if (_isTransitioningScene) return; // Prevent double-trigger from UI Event System + Input System
            if (Time.unscaledTime - _lastClickTime < 0.05f) return; // Prevent double-trigger from UI Event System + Input System
            _lastClickTime = Time.unscaledTime;
            CancelAutoPlayTimer();

            Debug.Log($"[DialogueUI] OnClick triggered. isTyping={isTyping}");
            if (isTyping)
            {
                SkipTyping();
            }
            else
            {
                // ADDED: 1-second delay check after typing is finished
                if (Time.unscaledTime - _typingEndTime < 0.3f)
                {
                    Debug.Log($"[DialogueUI] Advance ignored due to 0.3-second cooldown.");
                    return;
                }

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










