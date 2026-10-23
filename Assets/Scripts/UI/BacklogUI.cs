using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using System.Collections.Generic;
using HalloweenVN.Core;
using HalloweenVN.Dialogue;
using HalloweenVN.Data;
using HalloweenVN.UI.Theme;

namespace HalloweenVN.UI
{
    public class BacklogUI : MonoBehaviour
    {
        [SerializeField] private GameObject backlogPanel;
        [SerializeField] private Transform contentContainer;
        [SerializeField] private GameObject backlogEntryPrefab;
        [SerializeField] private Button closeButton;
        [SerializeField] private ScrollRect scrollRect;
        [SerializeField] private TextMeshProUGUI titleText;
        [SerializeField] private Text closeButtonText;

        private static List<BacklogEntry> history = new List<BacklogEntry>();
        private bool subscribedToDialogue = false;
        private bool subscribedToPhase = false;
        private int _openedFrame = -1;
        private Coroutine _scrollBottomCoroutine;

        public class BacklogEntry
        {
            public string dialogueId;
            public DialogueNode node;
            public string speaker;
            public string text;

            public BacklogEntry(string dialogueId, DialogueNode node)
            {
                this.dialogueId = dialogueId;
                this.node = node;
                this.speaker = node.speaker;
                this.text = HalloweenVN.Core.Loc.NodeText(dialogueId, node);
            }
        }

        private void Start()
        {
            // Subscribe in Start to ensure managers are initialized
            TrySubscribe();
            if (closeButton != null)
            {
                closeButton.onClick.AddListener(HideBacklog);
            }
        }

        private void OnEnable()
        {
            // Re-subscribe if previously unsubscribed
            TrySubscribe();
        }

        private GameObject _activePopup; // Track active popup overlay for ESC dismissal
        private int _activePopupHistoryIndex = -1;
        private float _popupOpenedTime = 0f;

        public bool HasActivePopup => _activePopup != null;

        public void DismissActivePopup()
        {
            if (_activePopup != null)
            {
                Destroy(_activePopup);
                _activePopup = null;
                _activePopupHistoryIndex = -1;
            }
            ResetAllEntryHovers();
        }

        private void ResetAllEntryHovers()
        {
            for (int i = 0; i < _entryPool.Count; i++)
            {
                var v = _entryPool[i];
                if (v != null && v.root != null && v.root.activeSelf && v.hover != null)
                {
                    v.hover.ResetHover();
                }
            }
        }

        private void Update()
        {
            // Lazy subscription fallback
            if (!subscribedToDialogue || !subscribedToPhase)
            {
                TrySubscribe();
            }

            if (!IsOpen) return;

            var kb = UnityEngine.InputSystem.Keyboard.current;

            // Allow Backlog key (e.g. L) to toggle/close the backlog when no popup is open
            if (_activePopup == null && Time.frameCount > _openedFrame && SettingsData.WasBacklogKeyPressedThisFrame())
            {
                if (AudioManager.Instance != null) AudioManager.Instance.PlaySFX("sfx_ui_click");
                HideBacklog();
                return;
            }

            // Allow Enter/Space to confirm the rewind popup
            if (_activePopup != null && Time.unscaledTime - _popupOpenedTime >= 0.15f)
            {
                if (kb != null && (kb.enterKey.wasPressedThisFrame || kb.numpadEnterKey.wasPressedThisFrame || kb.spaceKey.wasPressedThisFrame))
                {
                    if (AudioManager.Instance != null) AudioManager.Instance.PlaySFX("sfx_ui_click");
                    int targetIdx = _activePopupHistoryIndex;
                    DismissActivePopup();
                    ExecuteRewind(targetIdx);
                    return;
                }
            }

            // Keyboard scroll while backlog is open
            if (_activePopup == null && scrollRect != null && kb != null && scrollRect.content != null)
            {
                float contentH = scrollRect.content.rect.height;
                float viewH = scrollRect.viewport != null ? scrollRect.viewport.rect.height : 800f;
                float scrollable = Mathf.Max(1f, contentH - viewH);
                float delta = 0f;
                if (kb.upArrowKey.isPressed) delta += (600f * Time.unscaledDeltaTime) / scrollable;
                if (kb.downArrowKey.isPressed) delta -= (600f * Time.unscaledDeltaTime) / scrollable;
                if (kb.pageUpKey.wasPressedThisFrame) delta += (viewH * 0.8f) / scrollable;
                if (kb.pageDownKey.wasPressedThisFrame) delta -= (viewH * 0.8f) / scrollable;
                if (Mathf.Abs(delta) > 0.0001f)
                {
                    scrollRect.velocity = Vector2.zero;
                    scrollRect.verticalNormalizedPosition = Mathf.Clamp01(scrollRect.verticalNormalizedPosition + delta);
                }
            }
        }

        private void TrySubscribe()
        {
            if (!subscribedToDialogue && DialogueManager.Instance != null)
            {
                DialogueManager.Instance.OnNodeDisplayed += RecordNode;
                subscribedToDialogue = true;
            }
            if (!subscribedToPhase && GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged += HandlePhaseChanged;
                subscribedToPhase = true;
            }
        }

        private void OnDisable()
        {
            // Only unsubscribe on destroy so dialogue recording stays active across panel toggles
        }

        private void OnDestroy()
        {
            // Final cleanup only on destroy
            if (subscribedToDialogue && DialogueManager.Instance != null)
            {
                DialogueManager.Instance.OnNodeDisplayed -= RecordNode;
                subscribedToDialogue = false;
            }
            if (subscribedToPhase && GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged -= HandlePhaseChanged;
                subscribedToPhase = false;
            }
            if (closeButton != null)
            {
                closeButton.onClick.RemoveListener(HideBacklog);
            }
        }

        private void RecordNode(DialogueNode node)
        {
            if (node == null) return;
            string currentDialogId = DialogueManager.Instance?.CurrentDialogueId;
            RecordNodeSilently(currentDialogId, node);
        }

        public static void RecordNodeSilently(string dialogueId, DialogueNode node)
        {
            if (node == null) return;
            string checkText = HalloweenVN.Core.Loc.NodeText(dialogueId, node);
            if (string.IsNullOrEmpty(checkText)) return;
            history.Add(new BacklogEntry(dialogueId, node));
            if (history.Count > 300)
            {
                history.RemoveAt(0);
            }
        }

        private void HandlePhaseChanged(GamePhase phase)
        {
            if (phase == GamePhase.Lobby)
            {
                HideBacklog();
                // Clear history when returning to lobby (new game)
                history.Clear();
            }
        }

        public bool IsOpen => backlogPanel != null && backlogPanel.activeSelf;

        public void ToggleBacklog()
        {
            if (backlogPanel != null)
            {
                if (backlogPanel.activeSelf)
                {
                    HideBacklog();
                }
                else
                {
                    ShowBacklog();
                }
            }
        }

        public void ShowBacklog()
        {
            if (backlogPanel == null) return;
            if (DialogueManager.Instance != null && (!DialogueManager.Instance.IsPlaying || DialogueManager.Instance.IsTransitioningChapter))
                return;
            var dui = Object.FindAnyObjectByType<DialogueUI>();
            if (dui != null && dui.IsTransitioningScene)
                return;

            _openedFrame = Time.frameCount;
            backlogPanel.SetActive(true);

            PopulateBacklog();
            RebuildAndScrollToBottom();

            if (gameObject.activeInHierarchy)
            {
                if (_scrollBottomCoroutine != null) StopCoroutine(_scrollBottomCoroutine);
                _scrollBottomCoroutine = StartCoroutine(EnsureScrollBottomNextFrame());
            }
        }

        private void RebuildAndScrollToBottom()
        {
            Canvas.ForceUpdateCanvases();
            if (contentContainer != null)
            {
                for (int i = 0; i < history.Count && i < _entryPool.Count; i++)
                {
                    if (_entryPool[i].root != null && _entryPool[i].root.activeSelf)
                    {
                        RectTransform entryRt = _entryPool[i].root.transform as RectTransform;
                        if (entryRt != null) LayoutRebuilder.ForceRebuildLayoutImmediate(entryRt);
                    }
                }
                RectTransform contentRt = contentContainer as RectTransform;
                if (contentRt != null) LayoutRebuilder.ForceRebuildLayoutImmediate(contentRt);
            }
            Canvas.ForceUpdateCanvases();
            if (scrollRect != null)
            {
                scrollRect.velocity = Vector2.zero;
                scrollRect.verticalNormalizedPosition = 0f; // Scroll to bottom
            }
        }

        private IEnumerator EnsureScrollBottomNextFrame()
        {
            yield return null;
            if (IsOpen && scrollRect != null)
            {
                if (contentContainer is RectTransform contentRt)
                {
                    LayoutRebuilder.ForceRebuildLayoutImmediate(contentRt);
                }
                scrollRect.velocity = Vector2.zero;
                scrollRect.verticalNormalizedPosition = 0f;
            }
            _scrollBottomCoroutine = null;
        }

        public void HideBacklog()
        {
            if (_scrollBottomCoroutine != null)
            {
                StopCoroutine(_scrollBottomCoroutine);
                _scrollBottomCoroutine = null;
            }
            DismissActivePopup();
            if (backlogPanel != null)
            {
                backlogPanel.SetActive(false);
            }
        }

        private class PooledEntryView
        {
            public GameObject root;
            public Image bgImage;
            public Outline outline;
            public GameObject speakerObj;
            public TextMeshProUGUI speakerText;
            public TextMeshProUGUI dialogueText;
            public GameObject tagObj;
            public TextMeshProUGUI tagText;
            public Button button;
            public BacklogEntryHover hover;
            public int entryIndex;
        }

        private readonly List<PooledEntryView> _entryPool = new List<PooledEntryView>();
        private GameObject _emptyMsgObj;
        private TextMeshProUGUI _emptyMsgText;
        private bool _containerLayoutInitialized = false;

        private PooledEntryView CreatePooledEntryView(int index)
        {
            var view = new PooledEntryView { entryIndex = index };

            GameObject entryObj = new GameObject($"BacklogEntry_{index}");
            entryObj.transform.SetParent(contentContainer, false);
            view.root = entryObj;

            view.bgImage = entryObj.AddComponent<Image>();
            view.outline = entryObj.AddComponent<Outline>();
            view.outline.effectDistance = new Vector2(3f, 3f);

            var layout = entryObj.AddComponent<VerticalLayoutGroup>();
            layout.padding = new RectOffset(32, 32, 18, 22);
            layout.spacing = 8;
            layout.childControlHeight = true;
            layout.childControlWidth = true;
            layout.childForceExpandHeight = false;
            layout.childForceExpandWidth = true;

            var entryCsf = entryObj.AddComponent<ContentSizeFitter>();
            entryCsf.verticalFit = ContentSizeFitter.FitMode.PreferredSize;

            // Speaker
            GameObject speakerObj = new GameObject("Speaker");
            speakerObj.transform.SetParent(entryObj.transform, false);
            var speakerTxt = speakerObj.AddComponent<TextMeshProUGUI>();
            speakerTxt.fontStyle = FontStyles.Bold;
            speakerTxt.fontSize = 30;
            speakerTxt.raycastTarget = false;
            view.speakerObj = speakerObj;
            view.speakerText = speakerTxt;

            // Dialogue / narration text
            GameObject textObj = new GameObject("Text");
            textObj.transform.SetParent(entryObj.transform, false);
            var dialogueTxt = textObj.AddComponent<TextMeshProUGUI>();
            dialogueTxt.fontSize = 28;
            dialogueTxt.textWrappingMode = TextWrappingModes.Normal;
            dialogueTxt.raycastTarget = false;
            view.dialogueText = dialogueTxt;

            // Top-right tag
            GameObject tagObj = new GameObject("Tag");
            tagObj.transform.SetParent(entryObj.transform, false);
            var tagLe = tagObj.AddComponent<LayoutElement>();
            tagLe.ignoreLayout = true;
            var tagRt = tagObj.GetComponent<RectTransform>();
            if (tagRt == null) tagRt = tagObj.AddComponent<RectTransform>();
            tagRt.anchorMin = new Vector2(1, 1);
            tagRt.anchorMax = new Vector2(1, 1);
            tagRt.pivot = new Vector2(1, 1);
            tagRt.anchoredPosition = new Vector2(-20, -14);
            tagRt.sizeDelta = new Vector2(360, 36);
            var tagTxt = tagObj.AddComponent<TextMeshProUGUI>();
            tagTxt.alignment = TextAlignmentOptions.TopRight;
            tagTxt.fontSize = 22;
            tagTxt.raycastTarget = false;
            view.tagObj = tagObj;
            view.tagText = tagTxt;

            var btn = entryObj.AddComponent<Button>();
            btn.targetGraphic = view.bgImage;
            btn.transition = Selectable.Transition.None;
            btn.onClick.AddListener(() => OnEntryClicked(view.entryIndex));
            view.button = btn;

            var hover = entryObj.AddComponent<BacklogEntryHover>();
            hover.background = view.bgImage;
            hover.outline = view.outline;
            hover.hint = tagObj;
            view.hover = hover;

            return view;
        }

        private void PopulateBacklog()
        {
            if (contentContainer == null) return;

            if (!_containerLayoutInitialized)
            {
                var vlg = contentContainer.GetComponent<VerticalLayoutGroup>();
                if (vlg == null)
                {
                    vlg = contentContainer.gameObject.AddComponent<VerticalLayoutGroup>();
                }
                vlg.padding = new RectOffset(20, 20, 16, 16);
                vlg.spacing = 14;
                vlg.childControlHeight = true;
                vlg.childControlWidth = true;
                vlg.childForceExpandHeight = false;
                vlg.childForceExpandWidth = true;

                var csf = contentContainer.GetComponent<ContentSizeFitter>();
                if (csf == null)
                {
                    csf = contentContainer.gameObject.AddComponent<ContentSizeFitter>();
                }
                csf.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
                _containerLayoutInitialized = true;
            }

            bool isGothic = !SettingsData.UseHandwritingFont;
            float speakerFontSize = isGothic ? 25f : 32f;
            float bodyFontSize = isGothic ? 23f : 30f;
            float tagFontSize = isGothic ? 18f : 23f;
            float titleFontSize = isGothic ? 28f : 36f;
            int closeBtnFontSize = isGothic ? 20 : 26;

            string globalFontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(SettingsData.Language);
            var cachedFont = HalloweenVN.UI.FontHelper.GetTMPFont(globalFontName);
            var legacyFont = HalloweenVN.UI.FontHelper.GetFont(globalFontName);

            if (titleText != null)
            {
                titleText.text = HalloweenVN.Core.Loc.Get("ui.builder.backlog.title", "대화 기록");
                titleText.fontSize = titleFontSize;
                if (cachedFont != null) titleText.font = cachedFont;
            }
            if (closeButtonText != null)
            {
                closeButtonText.text = HalloweenVN.Core.Loc.Get("ui.builder.close", "닫기");
                closeButtonText.fontSize = closeBtnFontSize;
                if (legacyFont != null) closeButtonText.font = legacyFont;
            }

            if (history.Count == 0)
            {
                for (int i = 0; i < _entryPool.Count; i++)
                {
                    if (_entryPool[i].root != null) _entryPool[i].root.SetActive(false);
                }

                if (_emptyMsgObj == null)
                {
                    _emptyMsgObj = new GameObject("EmptyMsg");
                    _emptyMsgObj.transform.SetParent(contentContainer, false);
                    _emptyMsgText = _emptyMsgObj.AddComponent<TextMeshProUGUI>();
                    _emptyMsgText.color = HalloweenTheme.TextPrimary;
                    _emptyMsgText.alignment = TextAlignmentOptions.Center;
                }
                _emptyMsgObj.SetActive(true);
                _emptyMsgText.text = HalloweenVN.Core.Loc.Get("ui.backlog.empty", "기록된 대화가 없습니다.");
                _emptyMsgText.fontSize = bodyFontSize;
                if (cachedFont != null) _emptyMsgText.font = cachedFont;
                return;
            }

            if (_emptyMsgObj != null) _emptyMsgObj.SetActive(false);

            string hintLabel = HalloweenVN.Core.Loc.Get("ui.backlog.rewind_hint", "◀ 이 장면으로 되감기");
            string currentLabel = HalloweenVN.Core.Loc.Get("ui.backlog.current", "현재");

            Color boxBg = HalloweenTheme.PanelBackground;
            Color boxBgHover = new Color(boxBg.r * 1.6f, boxBg.g * 1.6f, boxBg.b * 1.6f, Mathf.Min(1f, boxBg.a + 0.1f));
            Color narrationBg = new Color(boxBg.r * 0.6f, boxBg.g * 0.6f, boxBg.b * 0.6f, boxBg.a);
            Color dimBorder = new Color(HalloweenTheme.PanelBorder.r, HalloweenTheme.PanelBorder.g, HalloweenTheme.PanelBorder.b, 0.45f);
            Color narrationTextColor = new Color(HalloweenTheme.TextPrimary.r, HalloweenTheme.TextPrimary.g, HalloweenTheme.TextPrimary.b, 0.75f);

            for (int i = 0; i < history.Count; i++)
            {
                PooledEntryView view;
                if (i < _entryPool.Count && _entryPool[i].root != null)
                {
                    view = _entryPool[i];
                }
                else
                {
                    view = CreatePooledEntryView(i);
                    if (i < _entryPool.Count) _entryPool[i] = view;
                    else _entryPool.Add(view);
                }

                view.entryIndex = i;
                view.root.SetActive(true);

                var entry = history[i];
                bool isLastEntry = (i == history.Count - 1);
                bool isNarration = string.IsNullOrWhiteSpace(entry.speaker);
                string bodyText = ResolveText(entry);

                Color normalBg = isNarration ? narrationBg : boxBg;
                Color normalBorder = isLastEntry ? HalloweenTheme.AccentOrange : dimBorder;

                if (!isNarration)
                {
                    view.speakerObj.SetActive(true);
                    view.speakerText.text = HalloweenVN.Core.Loc.Speaker(entry.speaker);
                    view.speakerText.color = DialogueUI.GetSpeakerColor(entry.speaker);
                    view.speakerText.fontSize = speakerFontSize;
                    if (cachedFont != null) view.speakerText.font = cachedFont;
                }
                else
                {
                    view.speakerObj.SetActive(false);
                }

                view.dialogueText.text = bodyText;
                view.dialogueText.fontStyle = isNarration ? FontStyles.Italic : FontStyles.Normal;
                view.dialogueText.color = isNarration ? narrationTextColor : HalloweenTheme.TextPrimary;
                view.dialogueText.fontSize = bodyFontSize;
                if (cachedFont != null) view.dialogueText.font = cachedFont;

                if (cachedFont != null) view.tagText.font = cachedFont;
                view.tagText.color = HalloweenTheme.AccentOrange;
                view.tagText.fontSize = tagFontSize;
                view.tagText.text = isLastEntry ? currentLabel : hintLabel;

                view.hover.normalBg = normalBg;
                view.hover.hoverBg = boxBgHover;
                view.hover.normalBorder = normalBorder;
                view.hover.hoverBorder = HalloweenTheme.AccentOrange;
                view.hover.isCurrentEntry = isLastEntry;
                view.hover.enabled = !isLastEntry;
                view.button.enabled = !isLastEntry;
                view.hover.ResetHover();
            }

            for (int i = history.Count; i < _entryPool.Count; i++)
            {
                if (_entryPool[i].root != null) _entryPool[i].root.SetActive(false);
            }
        }
        
        /// <summary>Text for an entry in the CURRENT language (so a mid-game language switch updates past lines too).</summary>
        private static string ResolveText(BacklogEntry entry)
        {
            if (entry.node == null) return entry.text;
            return HalloweenVN.Core.Loc.NodeText(entry.dialogueId, entry.node);
        }
        
        private void OnEntryClicked(int historyIndex)
        {
            // Don't allow rewinding to the very last entry (current dialogue)
            if (historyIndex >= history.Count - 1) return;
            if (AudioManager.Instance != null) AudioManager.Instance.PlaySFX("sfx_ui_click");
            ShowRewindConfirmPopup(historyIndex);
        }

        private void ShowRewindConfirmPopup(int historyIndex)
        {
            // Destroy any existing popup first
            if (_activePopup != null) Destroy(_activePopup);
            ResetAllEntryHovers();

            bool isGothic = !SettingsData.UseHandwritingFont;

            // Create full screen overlay
            GameObject overlay = new GameObject("RewindPopupOverlay");
            overlay.transform.SetParent(backlogPanel.transform, false);
            _activePopup = overlay;
            _activePopupHistoryIndex = historyIndex;
            _popupOpenedTime = Time.unscaledTime;
            
            RectTransform overlayRt = overlay.AddComponent<RectTransform>();
            overlayRt.anchorMin = Vector2.zero;
            overlayRt.anchorMax = Vector2.one;
            overlayRt.offsetMin = Vector2.zero;
            overlayRt.offsetMax = Vector2.zero;
            
            Image bgImg = overlay.AddComponent<Image>();
            bgImg.color = new Color(0, 0, 0, 0.85f);
            
            // Overlay background click dismisses popup
            var btnOverlay = overlay.AddComponent<Button>();
            btnOverlay.transition = Selectable.Transition.None;
            btnOverlay.onClick.AddListener(() => {
                if (AudioManager.Instance != null) AudioManager.Instance.PlaySFX("sfx_ui_click");
                DismissActivePopup();
            });
            
            // Panel (Rounded Halloween modal card + click blocker so clicking inside doesn't cancel)
            GameObject panel = new GameObject("ConfirmPanel");
            panel.transform.SetParent(overlay.transform, false);
            RectTransform panelRt = panel.AddComponent<RectTransform>();
            panelRt.sizeDelta = new Vector2(680, 320);
            
            Image panelImg = panel.AddComponent<Image>();
            panelImg.type = Image.Type.Sliced;
            panelImg.sprite = UIHelper.CreateRoundedRectSprite(16, 2, new Color32(28, 18, 42, 255), HalloweenTheme.AccentOrange);

            Button panelBlockerBtn = panel.AddComponent<Button>();
            panelBlockerBtn.transition = Selectable.Transition.None;
            
            // Text
            GameObject textObj = new GameObject("Text");
            textObj.transform.SetParent(panel.transform, false);
            RectTransform textRt = textObj.AddComponent<RectTransform>();
            textRt.anchorMin = new Vector2(0, 0.38f);
            textRt.anchorMax = new Vector2(1, 1f);
            textRt.offsetMin = new Vector2(28, 0);
            textRt.offsetMax = new Vector2(-28, -24);
            
            int subSize = isGothic ? 20 : 24;
            TextMeshProUGUI tmp = textObj.AddComponent<TextMeshProUGUI>();
            tmp.text = HalloweenVN.Core.Loc.Get("ui.backlog.rewind_confirm", "이 시점으로 되감기 하시겠습니까?")
                + $"\n<size={subSize}><color=#c8bfd4>"
                + HalloweenVN.Core.Loc.Get("ui.backlog.rewind_warning", "(이후의 진행 내역은 사라집니다)")
                + "</color></size>";
            tmp.alignment = TextAlignmentOptions.Center;
            tmp.fontSize = isGothic ? 28f : 34f;
            tmp.lineSpacing = 8f;
            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(SettingsData.Language);
            var tmpFont = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            if (tmpFont != null) tmp.font = tmpFont;
            
            // Buttons (Distinct primary orange 'Yes' vs secondary dark purple 'No')
            var yesBtnTup = UIHelper.CreateButton(panel.transform, HalloweenVN.Core.Loc.Get("ui.common.yes", "예"), 210, 64);
            var noBtnTup = UIHelper.CreateButton(panel.transform, HalloweenVN.Core.Loc.Get("ui.common.no", "아니오"), 210, 64);

            Image yesImg = yesBtnTup.btn.GetComponent<Image>();
            if (yesImg != null)
            {
                yesImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, new Color32(195, 75, 20, 255), new Color32(255, 175, 80, 255));
                yesImg.type = Image.Type.Sliced;
                yesImg.color = Color.white;
                var ycb = yesBtnTup.btn.colors;
                ycb.normalColor = Color.white;
                ycb.highlightedColor = new Color32(255, 225, 190, 255);
                ycb.pressedColor = new Color32(180, 120, 90, 255);
                ycb.selectedColor = Color.white;
                yesBtnTup.btn.colors = ycb;
            }
            yesBtnTup.btnText.color = Color.white;
            yesBtnTup.btnText.fontStyle = FontStyles.Bold;

            Image noImg = noBtnTup.btn.GetComponent<Image>();
            if (noImg != null)
            {
                noImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, new Color32(55, 38, 78, 255), new Color32(130, 95, 165, 255));
                noImg.type = Image.Type.Sliced;
                noImg.color = Color.white;
                var ncb = noBtnTup.btn.colors;
                ncb.normalColor = Color.white;
                ncb.highlightedColor = new Color32(225, 210, 245, 255);
                ncb.pressedColor = new Color32(160, 140, 190, 255);
                ncb.selectedColor = Color.white;
                noBtnTup.btn.colors = ncb;
            }
            noBtnTup.btnText.color = HalloweenTheme.TextPrimary;
            
            float btnFontSize = isGothic ? 24f : 30f;
            yesBtnTup.btnText.fontSize = btnFontSize;
            noBtnTup.btnText.fontSize = btnFontSize;
            if (tmpFont != null) yesBtnTup.btnText.font = tmpFont;
            if (tmpFont != null) noBtnTup.btnText.font = tmpFont;
            
            var yesRt = yesBtnTup.btn.GetComponent<RectTransform>();
            yesRt.anchorMin = new Vector2(0.5f, 0);
            yesRt.anchorMax = new Vector2(0.5f, 0);
            yesRt.anchoredPosition = new Vector2(-130, 68);
            
            var noRt = noBtnTup.btn.GetComponent<RectTransform>();
            noRt.anchorMin = new Vector2(0.5f, 0);
            noRt.anchorMax = new Vector2(0.5f, 0);
            noRt.anchoredPosition = new Vector2(130, 68);
            
            // Click handlers
            noBtnTup.btn.onClick.AddListener(() => {
                if (AudioManager.Instance != null) AudioManager.Instance.PlaySFX("sfx_ui_click");
                DismissActivePopup();
            });
            
            yesBtnTup.btn.onClick.AddListener(() => {
                if (AudioManager.Instance != null) AudioManager.Instance.PlaySFX("sfx_ui_click");
                DismissActivePopup();
                ExecuteRewind(historyIndex);
            });
        }
        
        private void ExecuteRewind(int historyIndex)
        {
            if (historyIndex < 0 || historyIndex >= history.Count) return;
            
            var targetEntry = history[historyIndex];
            
            // Cut history up to BEFORE this point, because DisplayNode will record it again
            List<BacklogEntry> rewindHistory = new List<BacklogEntry>();
            for(int i = 0; i < historyIndex; i++)
            {
                rewindHistory.Add(history[i]);
            }
            
            history = rewindHistory;
            
            HideBacklog();
            DialogueManager.Instance.RewindTo(targetEntry.dialogueId, targetEntry.node, rewindHistory);
        }

        public static void ClearHistory()
        {
            history.Clear();
        }
    }
}
