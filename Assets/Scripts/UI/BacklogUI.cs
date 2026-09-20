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

        private void OnEnable()
        {
            if (DialogueManager.Instance != null)
            {
                DialogueManager.Instance.OnNodeDisplayed += RecordNode;
            }
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged += HandlePhaseChanged;
            }
            if (closeButton != null)
            {
                closeButton.onClick.AddListener(HideBacklog);
            }
        }

        private void OnDisable()
        {
            if (DialogueManager.Instance != null)
            {
                DialogueManager.Instance.OnNodeDisplayed -= RecordNode;
            }
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged -= HandlePhaseChanged;
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
            }
        }

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

        private void ShowBacklog()
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

        private void HideBacklog()
        {
            if (backlogPanel != null)
            {
                backlogPanel.SetActive(false);
            }
        }

        private void PopulateBacklog()
        {
            // Clear existing entries
            foreach (Transform child in contentContainer)
            {
                Destroy(child.gameObject);
            }

            string speakerHex = ColorUtility.ToHtmlStringRGB(HalloweenTheme.TextSpeaker);
            string textHex = ColorUtility.ToHtmlStringRGB(HalloweenTheme.TextPrimary);

            foreach (var entry in history)
            {
                GameObject newEntry = Instantiate(backlogEntryPrefab, contentContainer);
                TMP_Text tmpText = newEntry.GetComponentInChildren<TMP_Text>();
                if (tmpText != null)
                {
                    string speakerFormat = string.IsNullOrEmpty(entry.speaker) ? "" : $"<color=#{speakerHex}>{entry.speaker}</color>: ";
                    tmpText.text = $"{speakerFormat}<color=#{textHex}>{entry.text}</color>";
                }
            }
        }
    }
}
