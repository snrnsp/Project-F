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

        private class BacklogEntry
        {
            public string speaker;
            public string text;

            public BacklogEntry(string speaker, string text)
            {
                this.speaker = speaker;
                this.text = text;
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

        private void Update()
        {
            // Lazy subscription fallback: if DialogueManager wasn't ready at Start/OnEnable,
            // keep trying each frame until we successfully subscribe
            if (!subscribedToDialogue || !subscribedToPhase)
            {
                TrySubscribe();
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
            if (node == null || string.IsNullOrEmpty(node.text)) return;
            
            history.Add(new BacklogEntry(node.speaker, node.text));
            if (history.Count > 100)
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

            if (history.Count == 0)
            {
                // Show empty state message
                if (backlogEntryPrefab != null)
                {
                    GameObject emptyEntry = Instantiate(backlogEntryPrefab, contentContainer);
                    TMP_Text tmpText = emptyEntry.GetComponentInChildren<TMP_Text>();
                    if (tmpText != null)
                    {
                        string textHex = ColorUtility.ToHtmlStringRGB(HalloweenTheme.TextPrimary);
                        tmpText.text = $"<color=#{textHex}><i>기록된 대화가 없습니다.</i></color>";
                    }
                }
                return;
            }

            string speakerHex = ColorUtility.ToHtmlStringRGB(HalloweenTheme.TextSpeaker);
            string textHex2 = ColorUtility.ToHtmlStringRGB(HalloweenTheme.TextPrimary);

            foreach (var entry in history)
            {
                if (backlogEntryPrefab == null) break;
                
                GameObject newEntry = Instantiate(backlogEntryPrefab, contentContainer);
                TMP_Text tmpText = newEntry.GetComponentInChildren<TMP_Text>();
                if (tmpText != null)
                {
                    string speakerFormat = string.IsNullOrEmpty(entry.speaker) 
                        ? "" 
                        : $"<color=#{speakerHex}>{entry.speaker}</color>: ";
                    tmpText.text = $"{speakerFormat}<color=#{textHex2}>{entry.text}</color>";
                }
            }
        }

        /// <summary>
        /// Clear all recorded history (e.g., when starting a new game).
        /// </summary>
        public static void ClearHistory()
        {
            history.Clear();
        }
    }
}
