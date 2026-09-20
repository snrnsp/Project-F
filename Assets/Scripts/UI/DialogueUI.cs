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
    public class DialogueUI : MonoBehaviour
    {
        [SerializeField] private GameObject dialoguePanel;
        [SerializeField] private TextMeshProUGUI speakerNameText;
        [SerializeField] private TextMeshProUGUI dialogueText;
        [SerializeField] private Image characterImage;
        [SerializeField] private Image backgroundImage;
        [SerializeField] private GameObject choicePanel;
        [SerializeField] private GameObject choiceButtonPrefab;
        [SerializeField] private Transform choiceButtonContainer;
        [SerializeField] private float typingSpeed = 0.03f;
        [SerializeField] private Button autoButton;
        [SerializeField] private Button skipButton;
        [SerializeField] private Button backlogButton;
        [SerializeField] private TextMeshProUGUI autoButtonText;

        private Coroutine typingCoroutine;
        private Coroutine autoPlayCoroutine;
        private bool isTyping;
        private bool isAutoPlay;
        private string fullText;

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

        public void ShowDialoguePanel()
        {
            if (dialoguePanel != null)
                dialoguePanel.SetActive(true);
            ClearChoices();
        }

        public void HideDialoguePanel()
        {
            if (dialoguePanel != null)
                dialoguePanel.SetActive(false);
            ClearChoices();
            StopAutoPlay();
        }

        public void DisplayNode(DialogueNode node)
        {
            if (speakerNameText != null) speakerNameText.text = node.speaker;
            
            UpdateCharacterSprite(node.characterSprite);
            UpdateBackground(node.backgroundSprite);

            fullText = node.text ?? "";
            
            if (typingCoroutine != null)
            {
                StopCoroutine(typingCoroutine);
            }
            
            if (gameObject.activeInHierarchy)
            {
                typingCoroutine = StartCoroutine(TypeText(fullText));
            }
            else
            {
                dialogueText.text = fullText;
                isTyping = false;
            }
            
            ClearChoices();
        }

        private IEnumerator TypeText(string text)
        {
            isTyping = true;
            if (dialogueText != null) dialogueText.text = "";
            
            foreach (char c in text.ToCharArray())
            {
                if (dialogueText != null) dialogueText.text += c;
                yield return new WaitForSeconds(SettingsData.TextSpeed);
            }
            
            isTyping = false;

            // Auto-advance after typing completes
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

        public void SkipTyping()
        {
            if (typingCoroutine != null)
            {
                StopCoroutine(typingCoroutine);
            }
            if (dialogueText != null) dialogueText.text = fullText;
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
                if (btnText != null)
                {
                    btnText.text = choices[i].text;
                }

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

        private void UpdateCharacterSprite(string spritePath)
        {
            if (characterImage == null) return;
            if (!string.IsNullOrEmpty(spritePath))
            {
                Sprite sprite = Resources.Load<Sprite>(spritePath);
                if (sprite != null)
                {
                    characterImage.sprite = sprite;
                    characterImage.enabled = true;
                }
                else
                {
                    characterImage.enabled = false;
                }
            }
            else
            {
                characterImage.enabled = false;
            }
        }

        private void UpdateBackground(string spritePath)
        {
            if (backgroundImage == null) return;
            if (!string.IsNullOrEmpty(spritePath))
            {
                Sprite sprite = Resources.Load<Sprite>(spritePath);
                if (sprite != null)
                {
                    backgroundImage.sprite = sprite;
                    backgroundImage.enabled = true;
                }
            }
        }

        /// <summary>
        /// Toggles auto-play mode on/off.
        /// </summary>
        public void ToggleAutoPlay()
        {
            isAutoPlay = !isAutoPlay;
            if (autoButtonText != null)
            {
                autoButtonText.text = isAutoPlay ? "AUTO ON" : "AUTO";
            }

            // If turning on and not currently typing, start auto-advance
            if (isAutoPlay && !isTyping && DialogueManager.Instance != null && DialogueManager.Instance.IsPlaying)
            {
                autoPlayCoroutine = StartCoroutine(AutoAdvanceAfterDelay());
            }
        }

        /// <summary>
        /// Skips through dialogue quickly until choices appear or dialogue ends.
        /// </summary>
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
                yield return null; // Wait one frame
                DialogueManager.Instance.AdvanceDialogue();
                yield return null; // Wait one frame to check if choices appeared or dialogue ended
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
