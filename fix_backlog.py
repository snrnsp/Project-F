# Backlog System Diagnostic & Fix Script
# ============================================
# Issues found:
#
# 🔴 BUG 1: backlogModalRoot.SetActive(false) in OnPhaseChanged
#   - When any phase changes, backlogModalRoot (the root GO with BacklogUI component) is disabled
#   - BacklogUI.OnDisable() fires → unsubscribes OnNodeDisplayed event
#   - BacklogUI.OnEnable() only fires when the root is re-enabled, but nothing re-enables it!
#   - Result: After the first phase change, the backlog NEVER records new dialogue nodes
#
# 🔴 BUG 2: backlogPanel vs backlogModalRoot confusion  
#   - backlogPanel (inner panel) is what should be toggled for show/hide
#   - backlogModalRoot (outer root with BacklogUI component) should ALWAYS stay active
#   - OnPhaseChanged disables backlogModalRoot → kills the entire component lifecycle
#
# 🔴 BUG 3: OnEnable subscription timing
#   - BacklogUI subscribes to DialogueManager.Instance.OnNodeDisplayed in OnEnable()
#   - But DialogueManager might not exist yet when backlogRoot is first created in Awake()
#   - If DialogueManager.Instance is null at OnEnable time, subscription silently fails
#   - The subscription never retries → backlog permanently disconnected
#
# FIX STRATEGY:
# 1. Change OnPhaseChanged to toggle backlogPanel (inner panel) instead of backlogModalRoot
# 2. Change BacklogUI to subscribe in Start() or use lazy subscription pattern
# 3. Keep backlogModalRoot always active so OnNodeDisplayed events are always captured

import sys
sys.stdout.reconfigure(encoding='utf-8')

# === Fix 1: HalloweenUIBuilder.cs — stop disabling backlogModalRoot ===
path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Remove backlogModalRoot from OnPhaseChanged — the backlog should stay active to record
old = """            // Close all modal overlays on phase change to prevent them from blocking input
            if (settingsModalRoot) settingsModalRoot.SetActive(false);
            if (languageModalRoot) languageModalRoot.SetActive(false);
            if (backlogModalRoot) backlogModalRoot.SetActive(false);
            if (extraModalRoot) extraModalRoot.SetActive(false);"""

new = """            // Close all modal overlays on phase change to prevent them from blocking input
            if (settingsModalRoot) settingsModalRoot.SetActive(false);
            if (languageModalRoot) languageModalRoot.SetActive(false);
            if (extraModalRoot) extraModalRoot.SetActive(false);
            // Note: backlogModalRoot is NOT disabled here — BacklogUI must stay active
            // to keep recording dialogue via OnNodeDisplayed. Only the inner panel is hidden.
            if (backlogUiRef != null && backlogUiRef.IsOpen) backlogUiRef.HideBacklog();"""

if old in content:
    content = content.replace(old, new)
    print("✅ Fix 1: OnPhaseChanged — backlogModalRoot 비활성화 제거, 대신 HideBacklog() 호출")
else:
    print("❌ Fix 1 실패: 대상 코드를 찾을 수 없음")

# Also make sure backlogPanel starts hidden but backlogRoot stays active
# Currently line 1073: backlogPanel.SetActive(false) — this is correct, keep it

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)

# === Fix 2: BacklogUI.cs — robust subscription with fallback ===
path = 'F:/Project-F/Assets/Scripts/UI/BacklogUI.cs'

new_content = '''using UnityEngine;
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
'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ Fix 2: BacklogUI.cs 전면 재작성")
print("   - Start()에서 구독 (OnEnable 대신)")
print("   - Update() lazy 구독 fallback (DialogueManager 지연 초기화 대응)")
print("   - OnDisable()에서 구독 해제하지 않음 (GO가 잠깐 꺼져도 기록 유지)")
print("   - OnDestroy()에서만 최종 정리")
print("   - Lobby 복귀 시 history.Clear()")
print("   - 빈 기록일 때 '기록된 대화가 없습니다' 표시")
print("   - null 체크 강화")

print("\n═══ 백로그 시스템 수정 완료 ═══")
