using System.Collections;
using System.Collections.Generic;
using UnityEngine;
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
        [SerializeField] private TextMeshProUGUI autoButtonText;

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
        private const float MOVE_DURATION = 0.5f;

        private Coroutine[] _moveCoroutines = new Coroutine[3];
        private Dictionary<Image, Coroutine> _highlightCoroutines = new Dictionary<Image, Coroutine>();
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
            narratorObj.transform.SetParent(transform, false);
            
            RectTransform rt = narratorObj.AddComponent<RectTransform>();
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;

            Image img = narratorObj.AddComponent<Image>();
            img.color = Color.black; // Solid black background for centered monologues

            Button btn = narratorObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.None;
            btn.onClick.AddListener(OnClick);

            // Child: text label (separate GameObject to avoid Graphic conflict)
            GameObject textObj = new GameObject("NarratorLabel");
            textObj.transform.SetParent(narratorObj.transform, false);

            RectTransform textRt = textObj.AddComponent<RectTransform>();
            textRt.anchorMin = Vector2.zero;
            textRt.anchorMax = Vector2.one;
            textRt.offsetMin = new Vector2(100, 100);
            textRt.offsetMax = new Vector2(-100, -100);

            narratorText = textObj.AddComponent<TextMeshProUGUI>();
            
            TMP_FontAsset font = null;
            if (dialogueText != null && dialogueText.font != null)
                font = dialogueText.font;
            if (font == null)
                font = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
            if (font == null)
                font = TMP_Settings.defaultFontAsset;
            
            if (font != null) narratorText.font = font;
            narratorText.fontSize = (dialogueText != null && dialogueText.fontSize > 0) ? dialogueText.fontSize : 36f;
            narratorText.color = Color.white;
            narratorText.alignment = TextAlignmentOptions.Center;
            narratorText.enableWordWrapping = true;
            narratorText.raycastTarget = false; // let clicks pass through to parent Button
            
            narratorObj.SetActive(false);
        }

        // ═══════════ Events ═══════════
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

            // Collect all requested characters for this node
            List<(string path, string baseName)> requestedChars = new List<(string, string)>();
            if (!string.IsNullOrEmpty(spriteLeft)) requestedChars.Add((spriteLeft, ExtractBaseName(spriteLeft)));
            if (!string.IsNullOrEmpty(spriteCenter)) requestedChars.Add((spriteCenter, ExtractBaseName(spriteCenter)));
            if (!string.IsNullOrEmpty(spriteRight)) requestedChars.Add((spriteRight, ExtractBaseName(spriteRight)));

            // Auto-assign positions for each character
            foreach (var (path, baseName) in requestedChars)
            {
                if (!_activeSpeakerPositions.ContainsKey(baseName))
                {
                    // New character — assign a free slot
                    CharacterPosition assignedPos;
                    if (_activeSpeakerPositions.Count >= 3)
                    {
                        // Evict oldest character
                        string oldest = _speakerOrder[0];
                        assignedPos = _activeSpeakerPositions[oldest];
                        FadeOutCharacter(assignedPos);
                        _activeSpeakerPositions.Remove(oldest);
                        _speakerOrder.RemoveAt(0);
                    }
                    else
                    {
                        assignedPos = FindFreeSlot();
                    }

                    _activeSpeakerPositions[baseName] = assignedPos;
                    _speakerOrder.Add(baseName);

                    // Load sprite & Fade In
                    Image img = GetCharacterImage(assignedPos);
                    LoadSpriteToImage(img, path);
                    StartCoroutine(FadeInCharacter(img));
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

            // Remove characters that are no longer in this node
            List<string> toRemove = new List<string>();
            foreach (var kvp in _activeSpeakerPositions)
            {
                bool found = false;
                foreach (var (path, baseName) in requestedChars)
                {
                    if (baseName == kvp.Key) { found = true; break; }
                }
                if (!found) toRemove.Add(kvp.Key);
            }
            foreach (string name in toRemove)
            {
                FadeOutCharacter(_activeSpeakerPositions[name]);
                _activeSpeakerPositions.Remove(name);
                _speakerOrder.Remove(name);
            }

            // Recalculate layout positions (smooth slide)
            UpdateCharacterLayout();

            // Dim/Highlight based on speaker
            UpdateSpeakerHighlight(node.speaker);

            // Background
            UpdateBackground(node.backgroundSprite);

            // Typing & Formatting
            fullText = node.text ?? "";
            bool isNarrator = string.IsNullOrEmpty(node.speaker);
            
            // Rule: Monologues with a background image use the dialogue panel.
            bool hasBackground = (backgroundImage != null && backgroundImage.sprite != null && backgroundImage.color.a > 0.01f);
            bool usePanel = !isNarrator || hasBackground;

            TextMeshProUGUI activeText = usePanel ? dialogueText : narratorText;

            if (usePanel)
            {
                // Show dialogue panel, hide narrator
                if (dialoguePanel != null) dialoguePanel.SetActive(true);
                if (narratorText != null && narratorText.transform.parent != null)
                {
                    narratorText.transform.parent.gameObject.SetActive(false);
                }
                if (dialogueText != null) dialogueText.alignment = TextAlignmentOptions.TopLeft;
            }
            else
            {
                EnsureNarratorText();
                // Hide dialogue panel, show fullscreen narrator
                if (dialoguePanel != null) dialoguePanel.SetActive(false);
                if (narratorText != null && narratorText.transform.parent != null)
                {
                    narratorText.transform.parent.gameObject.SetActive(true);
                }
                fullText = "<b>" + fullText + "</b>";
            }

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
                if (n == 2) targetX = (i == 0) ? 0.34f : 0.78f;
                else if (n == 3) targetX = (i == 0) ? 0.24f : (i == 1 ? 0.56f : 0.88f);

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
                StartCoroutine(FadeOutCharacterCoroutine(img));
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
        private void UpdateSpeakerHighlight(string speaker)
        {
            if (string.IsNullOrWhiteSpace(speaker))
            {
                // Narrator — all active characters stay bright
                foreach (var kvp in _activeSpeakerPositions)
                {
                    DimCharacterImage(GetCharacterImage(kvp.Value), true);
                }
                return;
            }

            foreach (var kvp in _activeSpeakerPositions)
            {
                bool isSpeaking = kvp.Key == speaker;
                DimCharacterImage(GetCharacterImage(kvp.Value), isSpeaking);
            }
        }

        private void DimCharacterImage(Image image, bool isActive, float duration = 0.2f)
        {
            if (image == null) return;
            if (!image.gameObject.activeSelf) return;

            Color targetColor = isActive ? ACTIVE_COLOR : DIM_COLOR;

            if (_highlightCoroutines.ContainsKey(image) && _highlightCoroutines[image] != null)
            {
                StopCoroutine(_highlightCoroutines[image]);
            }
            _highlightCoroutines[image] = StartCoroutine(FadeColorCoroutine(image, targetColor, duration));
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
            isTyping = true;
            if (target != null)
            {
                target.text = text;
                target.maxVisibleCharacters = 0;
            }

            // Yield once so TMPro can calculate the mesh and character counts
            yield return null;

            int totalVisibleChars = target != null ? target.textInfo.characterCount : 0;
            int visibleCount = 0;

            while (visibleCount <= totalVisibleChars && target != null)
            {
                target.maxVisibleCharacters = visibleCount;
                visibleCount++;
                yield return new WaitForSeconds(SettingsData.TextSpeed);
            }

            isTyping = false;

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
            if (typingCoroutine != null) StopCoroutine(typingCoroutine);
            if (dialogueText != null) dialogueText.maxVisibleCharacters = 99999;
            if (narratorText != null) narratorText.maxVisibleCharacters = 99999;
            isTyping = false;
        }

        public void OnClick()
        {
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
                autoButtonText.text = isAutoPlay ? "AUTO ON" : "AUTO";
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
            if (autoButtonText != null) autoButtonText.text = "AUTO";
            if (autoPlayCoroutine != null)
            {
                StopCoroutine(autoPlayCoroutine);
                autoPlayCoroutine = null;
            }
        }
    }
}
