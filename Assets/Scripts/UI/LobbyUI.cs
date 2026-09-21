using UnityEngine;
using UnityEngine.UI;
using TMPro;
using HalloweenVN.Core;
using HalloweenVN.Dialogue;

namespace HalloweenVN.UI
{
    /// <summary>
    /// Manages the lobby (title) screen UI.
    /// </summary>
    public class LobbyUI : MonoBehaviour
    {
        [SerializeField] private GameObject lobbyPanel;
        [SerializeField] private TextMeshProUGUI titleText;
        [SerializeField] private TextMeshProUGUI subtitleText;
        [SerializeField] private Button newGameButton;
        [SerializeField] private Button continueButton;

        private void OnEnable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged += HandlePhaseChanged;
            }
            UpdateContinueButton();
        }

        private void Start()
        {
            if (newGameButton != null)
            {
                newGameButton.onClick.AddListener(OnNewGameClicked);
            }
            if (continueButton != null)
            {
                continueButton.onClick.AddListener(OnContinueClicked);
            }
            UpdateContinueButton();
        }

        private void OnDisable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged -= HandlePhaseChanged;
            }
        }

        private void OnDestroy()
        {
            if (newGameButton != null)
            {
                newGameButton.onClick.RemoveListener(OnNewGameClicked);
            }
            if (continueButton != null)
            {
                continueButton.onClick.RemoveListener(OnContinueClicked);
            }
        }

        private void HandlePhaseChanged(GamePhase phase)
        {
            if (lobbyPanel == null) return;

            if (phase == GamePhase.Lobby)
            {
                lobbyPanel.SetActive(true);
                UpdateContinueButton();
                StopAllCoroutines();
                StartCoroutine(SlideLobby(true));
            }
            else
            {
                StopAllCoroutines();
                StartCoroutine(SlideLobby(false));
            }
        }

        private System.Collections.IEnumerator SlideLobby(bool show)
        {
            RectTransform rt = lobbyPanel.GetComponent<RectTransform>();
            float duration = 0.5f;
            float time = 0f;
            
            // X offset: 0 for show, -1920 for hide (sliding left)
            Vector2 startPos = rt.anchoredPosition;
            Vector2 targetPos = show ? Vector2.zero : new Vector2(-1920, 0);

            while (time < duration)
            {
                time += Time.deltaTime;
                float t = Mathf.SmoothStep(0, 1, time / duration);
                rt.anchoredPosition = Vector2.Lerp(startPos, targetPos, t);
                yield return null;
            }
            rt.anchoredPosition = targetPos;

            if (!show)
            {
                lobbyPanel.SetActive(false);
            }
        }

        /// <summary>
        /// Shows or hides the continue button based on save data availability.
        /// </summary>
        private void UpdateContinueButton()
        {
            if (continueButton != null)
            {
                continueButton.interactable = SaveManager.HasSave(0);
            }
        }

        private void OnNewGameClicked()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.ChangePhase(GamePhase.Dialogue);
            }
            if (DialogueManager.Instance != null)
            {
                DialogueManager.Instance.StartDialogue("ch0_opening");
            }
        }

        private void OnContinueClicked()
        {
            SaveData data = SaveManager.Load(0);
            if (data != null && GameManager.Instance != null)
            {
                if (System.Enum.TryParse(data.currentPhase, out GamePhase phase))
                {
                    GameManager.Instance.ChangePhase(phase);
                }
                if (!string.IsNullOrEmpty(data.currentDialogueId) && DialogueManager.Instance != null)
                {
                    DialogueManager.Instance.StartDialogue(data.currentDialogueId);
                }
            }
        }
    }
}
