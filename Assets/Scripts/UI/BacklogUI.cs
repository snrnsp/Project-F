using UnityEngine;
using UnityEngine.UI;
using TMPro;
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

        private static List<BacklogEntry> history = new List<BacklogEntry>();
        private bool subscribedToDialogue = false;
        private bool subscribedToPhase = false;

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

        private void Update()
        {
            // Lazy subscription fallback
            if (!subscribedToDialogue || !subscribedToPhase)
            {
                TrySubscribe();
            }

            // ESC / Right-Click handling
            bool closeInput = false;
            if (UnityEngine.InputSystem.Keyboard.current != null && UnityEngine.InputSystem.Keyboard.current.escapeKey.wasPressedThisFrame) closeInput = true;
            if (UnityEngine.InputSystem.Mouse.current != null && UnityEngine.InputSystem.Mouse.current.rightButton.wasPressedThisFrame) closeInput = true;

            if (closeInput)
            {
                if (_activePopup != null)
                {
                    Destroy(_activePopup);
                    _activePopup = null;
                }
                else if (IsOpen)
                {
                    HideBacklog();
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
            // Only unsubscribe the phase handler, NOT the dialogue recording
            // This way even if the GO is briefly disabled, we don't lose the subscription flag
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
            string checkText = HalloweenVN.Core.Loc.NodeText(DialogueManager.Instance?.CurrentDialogueId, node);
            if (string.IsNullOrEmpty(checkText)) return;
            string currentDialogId = DialogueManager.Instance.CurrentDialogueId;
            history.Add(new BacklogEntry(currentDialogId, node));
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
            backlogPanel.SetActive(true);

            PopulateBacklog();
            
            // Force layout rebuild so ScrollRect can calculate its bounds
            Canvas.ForceUpdateCanvases();
            if (scrollRect != null)
            {
                scrollRect.verticalNormalizedPosition = 0f; // Scroll to bottom
            }
        }

        public void HideBacklog()
        {
            if (backlogPanel != null)
            {
                backlogPanel.SetActive(false);
            }
        }

        
        private void PopulateBacklog()
        {
            if (contentContainer == null) return;

            // Clear existing entries
            foreach (Transform child in contentContainer)
            {
                Destroy(child.gameObject);
            }
            
            // Make sure the content container has a VerticalLayoutGroup and ContentSizeFitter
            var vlg = contentContainer.GetComponent<VerticalLayoutGroup>();
            if (vlg == null)
            {
                vlg = contentContainer.gameObject.AddComponent<VerticalLayoutGroup>();
                vlg.padding = new RectOffset(20, 20, 20, 20);
                vlg.spacing = 15;
                vlg.childControlHeight = true;
                vlg.childControlWidth = true;
                vlg.childForceExpandHeight = false;
                vlg.childForceExpandWidth = true;
            }
            var csf = contentContainer.GetComponent<ContentSizeFitter>();
            if (csf == null)
            {
                csf = contentContainer.gameObject.AddComponent<ContentSizeFitter>();
                csf.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
            }

            if (history.Count == 0)
            {
                GameObject emptyMsg = new GameObject("EmptyMsg");
                emptyMsg.transform.SetParent(contentContainer, false);
                var text = emptyMsg.AddComponent<TextMeshProUGUI>();
                text.text = HalloweenVN.Core.Loc.Get("ui.backlog.empty", "기록된 대화가 없습니다.");
                text.color = HalloweenTheme.TextPrimary;
                text.alignment = TextAlignmentOptions.Center;
                
                string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(SettingsData.Language);
                var tmpFont = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
                if (tmpFont != null) text.font = tmpFont;
                return;
            }

            // Pre-compute font and strings once outside the loop
            string globalFontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(SettingsData.Language);
            var cachedFont = HalloweenVN.UI.FontHelper.GetTMPFont(globalFontName);
            string hintLabel = HalloweenVN.Core.Loc.Get("ui.backlog.rewind_hint", "◀ 이 장면으로 되감기");
            string currentLabel = HalloweenVN.Core.Loc.Get("ui.backlog.current", "현재");

            Color boxBg = HalloweenTheme.PanelBackground;
            Color boxBgHover = new Color(boxBg.r * 1.6f, boxBg.g * 1.6f, boxBg.b * 1.6f, Mathf.Min(1f, boxBg.a + 0.1f));
            Color narrationBg = new Color(boxBg.r * 0.6f, boxBg.g * 0.6f, boxBg.b * 0.6f, boxBg.a);
            Color dimBorder = new Color(HalloweenTheme.PanelBorder.r, HalloweenTheme.PanelBorder.g, HalloweenTheme.PanelBorder.b, 0.45f);

            for (int i = 0; i < history.Count; i++)
            {
                var entry = history[i];
                int entryIndex = i; // capture for closure
                bool isLastEntry = (i == history.Count - 1);
                bool isNarration = string.IsNullOrWhiteSpace(entry.speaker);
                string bodyText = ResolveText(entry);
                
                GameObject entryObj = new GameObject($"BacklogEntry_{i}");
                entryObj.transform.SetParent(contentContainer, false);
                
                // ── Box (mirrors the in-game dialogue panel) ──
                var img = entryObj.AddComponent<Image>();
                var outline = entryObj.AddComponent<Outline>();
                outline.effectDistance = new Vector2(3f, 3f);
                
                Color normalBg = isNarration ? narrationBg : boxBg;
                img.color = normalBg;
                outline.effectColor = isLastEntry ? HalloweenTheme.AccentOrange : dimBorder;
                
                var layout = entryObj.AddComponent<VerticalLayoutGroup>();
                layout.padding = new RectOffset(32, 32, 18, 22);
                layout.spacing = 8;
                layout.childControlHeight = true;
                layout.childControlWidth = true;
                layout.childForceExpandHeight = false;
                layout.childForceExpandWidth = true;
                
                var entryCsf = entryObj.AddComponent<ContentSizeFitter>();
                entryCsf.verticalFit = ContentSizeFitter.FitMode.PreferredSize;
                
                // ── Speaker name (same per-character color as the dialogue box) ──
                if (!isNarration)
                {
                    GameObject speakerObj = new GameObject("Speaker");
                    speakerObj.transform.SetParent(entryObj.transform, false);
                    var speakerTxt = speakerObj.AddComponent<TextMeshProUGUI>();
                    speakerTxt.text = HalloweenVN.Core.Loc.Speaker(entry.speaker);
                    speakerTxt.color = DialogueUI.GetSpeakerColor(entry.speaker);
                    speakerTxt.fontStyle = FontStyles.Bold;
                    speakerTxt.fontSize = 30;
                    speakerTxt.raycastTarget = false;
                    if (cachedFont != null) speakerTxt.font = cachedFont;
                }
                
                // ── Dialogue / narration text ──
                GameObject textObj = new GameObject("Text");
                textObj.transform.SetParent(entryObj.transform, false);
                var dialogueTxt = textObj.AddComponent<TextMeshProUGUI>();
                dialogueTxt.text = bodyText;
                dialogueTxt.fontSize = 28;
                dialogueTxt.raycastTarget = false;
                if (isNarration)
                {
                    dialogueTxt.fontStyle = FontStyles.Italic;
                    dialogueTxt.color = new Color(HalloweenTheme.TextPrimary.r, HalloweenTheme.TextPrimary.g, HalloweenTheme.TextPrimary.b, 0.75f);
                }
                else
                {
                    dialogueTxt.color = HalloweenTheme.TextPrimary;
                }
                if (cachedFont != null) dialogueTxt.font = cachedFont;
                
                // ── Top-right tag: "현재" on the current line, rewind hint on hover for past lines ──
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
                tagRt.sizeDelta = new Vector2(320, 36);
                var tagTxt = tagObj.AddComponent<TextMeshProUGUI>();
                tagTxt.alignment = TextAlignmentOptions.TopRight;
                tagTxt.fontSize = 22;
                tagTxt.raycastTarget = false;
                if (cachedFont != null) tagTxt.font = cachedFont;
                
                if (isLastEntry)
                {
                    // Current line — not clickable
                    tagTxt.text = currentLabel;
                    tagTxt.color = HalloweenTheme.AccentOrange;
                }
                else
                {
                    tagTxt.text = hintLabel;
                    tagTxt.color = HalloweenTheme.AccentOrange;
                    tagObj.SetActive(false);
                    
                    var btn = entryObj.AddComponent<Button>();
                    btn.targetGraphic = img;
                    btn.transition = Selectable.Transition.None; // visuals handled by BacklogEntryHover
                    btn.onClick.AddListener(() => OnEntryClicked(entryIndex));
                    
                    var hover = entryObj.AddComponent<BacklogEntryHover>();
                    hover.background = img;
                    hover.outline = outline;
                    hover.hint = tagObj;
                    hover.normalBg = normalBg;
                    hover.hoverBg = boxBgHover;
                    hover.normalBorder = dimBorder;
                    hover.hoverBorder = HalloweenTheme.AccentOrange;
                }
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
            ShowRewindConfirmPopup(historyIndex);
        }

        private void ShowRewindConfirmPopup(int historyIndex)
        {
            // Destroy any existing popup first
            if (_activePopup != null) Destroy(_activePopup);

            // Create full screen overlay
            GameObject overlay = new GameObject("RewindPopupOverlay");
            overlay.transform.SetParent(backlogPanel.transform, false);
            _activePopup = overlay;
            
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
                Destroy(overlay);
                _activePopup = null;
            });
            
            // Panel
            GameObject panel = new GameObject("ConfirmPanel");
            panel.transform.SetParent(overlay.transform, false);
            RectTransform panelRt = panel.AddComponent<RectTransform>();
            panelRt.sizeDelta = new Vector2(700, 350);
            
            Image panelImg = panel.AddComponent<Image>();
            panelImg.color = new Color32(25, 20, 30, 255);
            var outline = panel.AddComponent<Outline>();
            outline.effectColor = new Color32(200, 150, 50, 255);
            outline.effectDistance = new Vector2(3, 3);
            
            // Text
            GameObject textObj = new GameObject("Text");
            textObj.transform.SetParent(panel.transform, false);
            RectTransform textRt = textObj.AddComponent<RectTransform>();
            textRt.anchorMin = new Vector2(0, 0.4f);
            textRt.anchorMax = new Vector2(1, 1f);
            textRt.offsetMin = new Vector2(20, 0);
            textRt.offsetMax = new Vector2(-20, -20);
            
            TextMeshProUGUI tmp = textObj.AddComponent<TextMeshProUGUI>();
            tmp.text = HalloweenVN.Core.Loc.Get("ui.backlog.rewind_confirm", "이 시점으로 되감기 하시겠습니까?")
                + "\n<size=24><color=#aaaaaa>"
                + HalloweenVN.Core.Loc.Get("ui.backlog.rewind_warning", "(이후의 진행 내역은 사라집니다)")
                + "</color></size>";
            tmp.alignment = TextAlignmentOptions.Center;
            tmp.fontSize = 36;
            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(SettingsData.Language);
            var tmpFont = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            if (tmpFont != null) tmp.font = tmpFont;
            
            // Buttons
            var yesBtnTup = UIHelper.CreateButton(panel.transform, HalloweenVN.Core.Loc.Get("ui.common.yes", "예"), 200, 80);
            var noBtnTup = UIHelper.CreateButton(panel.transform, HalloweenVN.Core.Loc.Get("ui.common.no", "아니오"), 200, 80);
            
            yesBtnTup.btnText.fontSize = 32;
            noBtnTup.btnText.fontSize = 32;
            if (tmpFont != null) yesBtnTup.btnText.font = tmpFont;
            if (tmpFont != null) noBtnTup.btnText.font = tmpFont;
            
            var yesRt = yesBtnTup.btn.GetComponent<RectTransform>();
            yesRt.anchorMin = new Vector2(0.5f, 0);
            yesRt.anchorMax = new Vector2(0.5f, 0);
            yesRt.anchoredPosition = new Vector2(-150, 100);
            
            var noRt = noBtnTup.btn.GetComponent<RectTransform>();
            noRt.anchorMin = new Vector2(0.5f, 0);
            noRt.anchorMax = new Vector2(0.5f, 0);
            noRt.anchoredPosition = new Vector2(150, 100);
            
            // Click handlers
            noBtnTup.btn.onClick.AddListener(() => {
                Destroy(overlay);
                _activePopup = null;
            });
            
            yesBtnTup.btn.onClick.AddListener(() => {
                Destroy(overlay);
                _activePopup = null;
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
