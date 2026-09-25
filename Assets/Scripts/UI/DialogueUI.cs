﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿using System.Collections;
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
        [SerializeField] private Button skipButton;
        [SerializeField] private Button backlogButton;

        [SerializeField] private Text autoButtonText;
        [SerializeField] private Text skipButtonText;
        [SerializeField] private Text backlogButtonText;
// ═══════════ Typing & Auto ═══════════
        private Coroutine typingCoroutine;
        private Coroutine autoPlayCoroutine;
        private bool isTyping;
        private bool isAutoPlay;
        private string fullText;

        // ═══════════ Character Position System (ported from old project) ═══════════
        private static readonly Color DIM_COLOR = new Color(0.45f, 0.45f, 0.45f, 1f);
        private static readonly Color ACTIVE_COLOR = Color.white;
        private const float DEFAULT_FADE_SPEED = 0.35f;
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
            if (dialogueText != null && dialogueText.font != null)
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
        
        public void UpdateLanguage()
        {

            if (skipButtonText != null) skipButtonText.resizeTextForBestFit = false;
            if (backlogButtonText != null) backlogButtonText.resizeTextForBestFit = false;
            if (autoButtonText != null) autoButtonText.resizeTextForBestFit = false;
            
            if (skipButtonText != null) skipButtonText.fontSize = 20;
            if (backlogButtonText != null) backlogButtonText.fontSize = 20;
            if (autoButtonText != null) autoButtonText.fontSize = 20;

            if (skipButtonText == null) return;
            var lang = HalloweenVN.Core.SettingsData.Language;
            string autoOff = "AUTO";
            string autoOn = "AUTO ON";
            
            if (lang == HalloweenVN.Core.GameLanguage.Korean)
            {
                autoOff = "오토"; autoOn = "오토 중";
                skipButtonText.text = "스킵";
                backlogButtonText.text = "로그";
            }
            else if (lang == HalloweenVN.Core.GameLanguage.English)
            {
                autoOff = "AUTO"; autoOn = "AUTO ON";
                skipButtonText.text = "SKIP";
                backlogButtonText.text = "LOG";
            }
            else if (lang == HalloweenVN.Core.GameLanguage.Japanese)
            {
                autoOff = "オート"; autoOn = "オート中";
                skipButtonText.text = "スキップ";
                backlogButtonText.text = "ログ";
            }
            else if (lang == HalloweenVN.Core.GameLanguage.ChineseSimplified)
            {
                autoOff = "自动"; autoOn = "自动中";
                skipButtonText.text = "跳过";
                backlogButtonText.text = "记录";
            }
            else if (lang == HalloweenVN.Core.GameLanguage.ChineseTraditional)
            {
                autoOff = "自動"; autoOn = "自動中";
                skipButtonText.text = "跳過";
                backlogButtonText.text = "紀錄";
            }
            
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
            if (skipButton != null) skipButton.onClick.AddListener(SkipAll);
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
            if (skipButton != null) skipButton.onClick.RemoveListener(SkipAll);
            StopAutoPlay();
        }

        // ═══════════ Panel Show/Hide ═══════════
        public void ShowDialoguePanel()
        {
            if (dialoguePanel != null)
                dialoguePanel.SetActive(true);
            ClearChoices();
            // Reset character tracking on new dialogue
            _activeSpeakerPositions.Clear();
            _speakerOrder.Clear();
        }

        public void HideDialoguePanel()
        {
            if (dialoguePanel != null)
                dialoguePanel.SetActive(false);
            ClearChoices();
            StopAutoPlay();
            HideAllCharacters();
        }

        // ═══════════ Display Node ═══════════


        public void DisplayNode(DialogueNode node)
        {

            if (speakerNameText != null) speakerNameText.text = node.speaker;

            // Determine which character sprites are requested
            string spriteLeft = node.characterSpriteLeft;
            string spriteCenter = node.characterSpriteCenter;
            string spriteRight = node.characterSpriteRight;

            // Legacy single-sprite support
            if (!string.IsNullOrEmpty(node.characterSprite))
            {
                spriteLeft = "";
                spriteCenter = node.characterSprite;
                spriteRight = "";
            }

            // Collect all requested characters for this node with their explicit positions
            List<(string path, string baseName, CharacterPosition? explicitPos)> requestedChars = new List<(string, string, CharacterPosition?)>();
            if (!string.IsNullOrEmpty(spriteLeft)) requestedChars.Add((spriteLeft, ExtractBaseName(spriteLeft), CharacterPosition.Left));
            if (!string.IsNullOrEmpty(spriteCenter)) requestedChars.Add((spriteCenter, ExtractBaseName(spriteCenter), CharacterPosition.Center));
            if (!string.IsNullOrEmpty(spriteRight)) requestedChars.Add((spriteRight, ExtractBaseName(spriteRight), CharacterPosition.Right));

            // Remove characters that are no longer in this node FIRST
            List<string> toRemove = new List<string>();
            foreach (var kvp in _activeSpeakerPositions)
            {
                bool found = false;
                foreach (var (path, baseName, explicitPos) in requestedChars)
                {
                    if (baseName == kvp.Key) { found = true; break; }
                }
                if (!found) toRemove.Add(kvp.Key);
            }
            foreach (string name in toRemove)
            {
                if (node.noFade)
                {
                    // Instant hide
                    Image hideImg = GetCharacterImage(_activeSpeakerPositions[name]);
                    if (hideImg != null) 
                    {
                        if (_fadeCoroutines.ContainsKey(hideImg) && _fadeCoroutines[hideImg] != null) StopCoroutine(_fadeCoroutines[hideImg]);
                        hideImg.gameObject.SetActive(false);
                    }
                }
                else
                {
                    FadeOutCharacter(_activeSpeakerPositions[name]);
                }
                _activeSpeakerPositions.Remove(name);
                _speakerOrder.Remove(name);
            }

            // Calculate target layout positions BEFORE placing characters
            int totalChars = requestedChars.Count;
            Dictionary<CharacterPosition, float> layoutTargets = new Dictionary<CharacterPosition, float>();
            if (totalChars == 1)
            {
                CharacterPosition? pos = requestedChars[0].explicitPos;
                layoutTargets[pos ?? CharacterPosition.Center] = 0.5f;
            }
            else if (totalChars == 2)
            {
                var sorted = new List<CharacterPosition?>();
                foreach (var rc in requestedChars) sorted.Add(rc.explicitPos);
                sorted.Sort((a, b) => (a ?? CharacterPosition.Center).CompareTo(b ?? CharacterPosition.Center));
                layoutTargets[sorted[0] ?? CharacterPosition.Left] = 0.25f;
                layoutTargets[sorted[1] ?? CharacterPosition.Right] = 0.75f;
            }
            else if (totalChars >= 3)
            {
                var sorted = new List<CharacterPosition?>();
                foreach (var rc in requestedChars) sorted.Add(rc.explicitPos);
                sorted.Sort((a, b) => (a ?? CharacterPosition.Center).CompareTo(b ?? CharacterPosition.Center));
                layoutTargets[sorted[0] ?? CharacterPosition.Left] = 0.20f;
                layoutTargets[sorted[1] ?? CharacterPosition.Center] = 0.50f;
                layoutTargets[sorted[2] ?? CharacterPosition.Right] = 0.80f;
            }

            // Now assign positions and place characters
            bool anyNewCharacter = false;
            foreach (var (path, baseName, explicitPos) in requestedChars)
            {
                CharacterPosition assignedPos = explicitPos ?? CharacterPosition.Center;

                if (!_activeSpeakerPositions.ContainsKey(baseName))
                {
                    anyNewCharacter = true;
                    // New character — place directly at final layout position
                    if (_activeSpeakerPositions.Count >= 3)
                    {
                        // Evict oldest character
                        string oldest = _speakerOrder[0];
                        CharacterPosition oldPos = _activeSpeakerPositions[oldest];
                        if (node.noFade)
                        {
                            Image hideImg = GetCharacterImage(oldPos);
                            if (hideImg != null) hideImg.gameObject.SetActive(false);
                        }
                        else
                        {
                            FadeOutCharacter(oldPos);
                        }
                        _activeSpeakerPositions.Remove(oldest);
                        _speakerOrder.RemoveAt(0);
                    }

                    _activeSpeakerPositions[baseName] = assignedPos;
                    _speakerOrder.Add(baseName);

                    // Load sprite & place at final position immediately
                    Image img = GetCharacterImage(assignedPos);
                    LoadSpriteToImage(img, path);

                    // Set initial position
                    if (layoutTargets.ContainsKey(assignedPos))
                    {
                        RectTransform rt = img.rectTransform;
                        float targetX = layoutTargets[assignedPos];
                        
                        bool isFirst = _activeSpeakerPositions.Count == 1;
                        if (node.slideIn || !isFirst)
                        {
                            // Start from off-screen (left or right depending on target position)
                            float offScreenX = (targetX < 0.5f) ? -0.5f : (targetX > 0.5f ? 1.5f : -0.5f);
                            
                            // 명시적으로 slideFromRight가 true이면 중앙 캐릭터라도 오른쪽에서 등장
                            if (node.slideFromRight) offScreenX = 1.5f;

                            SetCharacterAnchorX(rt, offScreenX);
                            MoveCharacterTo(assignedPos, targetX);
                        }
                        else
                        {
                            SetCharacterAnchorX(rt, targetX);
                        }
                    }

                    if (node.noFade)
                    {
                        if (_fadeCoroutines.ContainsKey(img) && _fadeCoroutines[img] != null) StopCoroutine(_fadeCoroutines[img]);
                        img.gameObject.SetActive(true);
                        Color c = img.color;
                        c.a = 1f;
                        img.color = c;
                    }
                    else
                    {
                        StartFadeIn(img);
                    }
                }
                else
                {
                    // Existing character — update sprite if changed, refresh order
                    _speakerOrder.Remove(baseName);
                    _speakerOrder.Add(baseName);

                    CharacterPosition pos = _activeSpeakerPositions[baseName];
                    Image img = GetCharacterImage(pos);
                    LoadSpriteToImage(img, path);
                }
            }

            // Recalculate layout positions for existing characters that need to shift
            if (anyNewCharacter)
            {
                foreach (var kvp in _activeSpeakerPositions)
                {
                    if (layoutTargets.ContainsKey(kvp.Value))
                    {
                        Image img = GetCharacterImage(kvp.Value);
                        if (img != null && img.gameObject.activeSelf)
                        {
                            RectTransform rt = img.rectTransform;
                            float currentX = (rt.anchorMin.x + rt.anchorMax.x) / 2f;
                            float targetX = layoutTargets[kvp.Value];
                            if (Mathf.Abs(currentX - targetX) > 0.01f)
                            {
                                MoveCharacterTo(kvp.Value, targetX);
                            }
                        }
                    }
                }
            }
            else
            {
                UpdateCharacterLayout();
            }

            // Dim/Highlight based on speaker
            bool wasNarrator = !_currentlyInDialoguePanel;
            bool isNarratorNow = string.IsNullOrEmpty(node.speaker);
            bool usePanelNow = !isNarratorNow;
            bool instantHighlight = wasNarrator && usePanelNow; // 컷신(독백)에서 대화로 넘어올 때는 깜빡임 방지를 위해 즉시 색상 적용
            UpdateSpeakerHighlight(node.speaker, instantHighlight);

            // Background
            UpdateBackground(node.backgroundSprite);

            // Typing & Formatting
            fullText = node.text ?? "";
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

            _tempPositionList.Clear();
            foreach (var v in _activeSpeakerPositions.Values) _tempPositionList.Add(v);
            _tempPositionList.Sort();

            int n = _tempPositionList.Count;
            for (int i = 0; i < n; i++)
            {
                float targetX = 0.5f; // Default: center
                if (n == 2) targetX = (i == 0) ? 0.25f : 0.75f;
                else if (n == 3) targetX = (i == 0) ? 0.20f : (i == 1 ? 0.50f : 0.80f);

                CharacterPosition pos = _tempPositionList[i];
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
                elapsed += Time.deltaTime;
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
        private void StartFadeIn(Image img)
        {
            if (img == null) return;
            if (_fadeCoroutines.ContainsKey(img) && _fadeCoroutines[img] != null) StopCoroutine(_fadeCoroutines[img]);
            _fadeCoroutines[img] = StartCoroutine(FadeInCharacter(img));
        }

        private IEnumerator FadeInCharacter(Image img)
        {
            if (img == null) yield break;

            img.gameObject.SetActive(true);
            Color c = img.color;
            c.a = 0f;
            img.color = c;

            yield return null; // 1 frame wait for layout

            float elapsed = 0f;
            while (elapsed < DEFAULT_FADE_SPEED)
            {
                elapsed += Time.deltaTime;
                c.a = Mathf.SmoothStep(0f, 1f, elapsed / DEFAULT_FADE_SPEED);
                img.color = c;
                yield return null;
            }
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
                elapsed += Time.deltaTime;
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
            Image[] chars = { characterImageLeft, characterImageCenter, characterImageRight };
            foreach (var img in chars)
            {
                if (img != null)
                {
                    img.gameObject.SetActive(false);
                    img.color = ACTIVE_COLOR;
                }
            }
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

            foreach (var kvp in _activeSpeakerPositions)
            {
                bool isSpeaking = kvp.Key == speaker;
                DimCharacterImage(GetCharacterImage(kvp.Value), isSpeaking, instant);
            }
        }

        private void DimCharacterImage(Image image, bool isActive, bool instant = false)
        {
            if (image == null) return;
            if (!image.gameObject.activeSelf) return;

            Color targetColor = isActive ? ACTIVE_COLOR : DIM_COLOR;
            float duration = instant ? 0f : 0.2f;

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
                elapsed += Time.deltaTime;
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
        private void LoadSpriteToImage(Image img, string spritePath)
        {
            if (img == null || string.IsNullOrEmpty(spritePath)) return;

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

            if (sprite != null)
            {
                img.sprite = sprite;
                img.enabled = true;
            }
        }

        // ═══════════ Background ═══════════
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
                    elapsed += Time.deltaTime;
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
                    elapsed += Time.deltaTime;
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

        private void UpdateBackground(string spritePath)
        {
            if (backgroundImage == null) return;
            if (!string.IsNullOrEmpty(spritePath))
            {
                Sprite sprite = Resources.Load<Sprite>(spritePath);

                if (sprite == null)
                {
                    Texture2D tex = Resources.Load<Texture2D>(spritePath);
                    if (tex != null)
                    {
                        sprite = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), new Vector2(0.5f, 0.5f));
                    }
                }

                if (sprite != null)
                {
                    backgroundImage.sprite = sprite;
                    backgroundImage.color = Color.white; // Ensure alpha is 1
                    backgroundImage.enabled = true;
                }
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

            if (target != null)
            {
                target.ForceMeshUpdate(true);
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
                        yield return new WaitForSeconds(0.7f);
                    }
                }
                
                visibleCount++;
                yield return new WaitForSeconds(SettingsData.TextSpeed);
            }

            isTyping = false;
            Debug.Log($"[DialogueUI] TypeText finished.");

            if (isAutoPlay)
            {
                autoPlayCoroutine = StartCoroutine(AutoAdvanceAfterDelay());
            }
        }

        private IEnumerator AutoAdvanceAfterDelay()
        {
            yield return new WaitForSeconds(SettingsData.AutoPlayDelay);
            if (isAutoPlay && DialogueManager.Instance != null)
            {
                DialogueManager.Instance.AdvanceDialogue();
            }
        }

        // ═══════════ Click / Input ═══════════
        public void SkipTyping()
        {
            Debug.Log($"[DialogueUI] SkipTyping called.");
            if (typingCoroutine != null) StopCoroutine(typingCoroutine);
            if (dialogueText != null) dialogueText.maxVisibleCharacters = 99999;
            if (narratorText != null) narratorText.maxVisibleCharacters = 99999;
            isTyping = false;
        }

        
        private bool isUiHidden = false;
        private bool _currentlyInDialoguePanel = true;
        

        private void Update()
        {
            if (GameManager.Instance != null && GameManager.Instance.CurrentPhase != GamePhase.Dialogue) return;
            if (choicePanel != null && choicePanel.activeSelf) return;

            // 1. Right click to toggle UI visibility (to see CG/Backgrounds)
            if (Mouse.current != null && Mouse.current.rightButton.wasPressedThisFrame)
            {
                isUiHidden = !isUiHidden;
                if (isUiHidden) StopAutoPlay();
                if (dialoguePanel != null) dialoguePanel.SetActive(!isUiHidden);
                if (autoButton != null) autoButton.gameObject.SetActive(!isUiHidden);
                if (skipButton != null) skipButton.gameObject.SetActive(!isUiHidden);
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
                    if (skipButton != null) skipButton.gameObject.SetActive(true);
                    if (backlogButton != null) backlogButton.gameObject.SetActive(true);
                }
                return;
            }

            // 2. Mouse Scroll Up to open Backlog
            if (Mouse.current != null && Mouse.current.scroll.ReadValue().y > 0)
            {
                var backlog = Object.FindFirstObjectByType<BacklogUI>(UnityEngine.FindObjectsInactive.Include);
                if (backlog != null && !backlog.IsOpen)
                {
                    backlog.ShowBacklog();
                }
            }

            // 3. Space / Enter to advance dialogue
            if ((Keyboard.current != null && Keyboard.current.spaceKey.wasPressedThisFrame) || (Keyboard.current != null && Keyboard.current.enterKey.wasPressedThisFrame))
            {
                OnClick();
            }
        }


        private float _lastClickTime = 0f;

        public void OnClick()
        {
            if (Time.unscaledTime - _lastClickTime < 0.05f) return; // Prevent double-trigger from UI Event System + Input System
            _lastClickTime = Time.unscaledTime;

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
                btnObj.SetActive(true);

                TextMeshProUGUI btnText = btnObj.GetComponentInChildren<TextMeshProUGUI>();
                if (btnText != null) btnText.text = choices[i].text;

                Button btn = btnObj.GetComponent<Button>();
                if (btn != null)
                {
                    btn.onClick.AddListener(() =>
                    {
                        ClearChoices();
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

            if (isAutoPlay && !isTyping && DialogueManager.Instance != null && DialogueManager.Instance.IsPlaying)
            {
                autoPlayCoroutine = StartCoroutine(AutoAdvanceAfterDelay());
            }
        }

        public void SkipAll()
        {
            StopAutoPlay();
            StartCoroutine(SkipCoroutine());
        }

        private IEnumerator SkipCoroutine()
        {
            while (DialogueManager.Instance != null && DialogueManager.Instance.IsPlaying)
            {
                SkipTyping();
                yield return null;
                DialogueManager.Instance.AdvanceDialogue();
                yield return null;
            }
        }

        private void StopAutoPlay()
        {
            isAutoPlay = false;
            if (autoButtonText != null) UpdateLanguage();
            if (autoPlayCoroutine != null)
            {
                StopCoroutine(autoPlayCoroutine);
                autoPlayCoroutine = null;
            }
        }
    }
}
