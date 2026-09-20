using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using HalloweenVN.Core;
using HalloweenVN.Data;

namespace HalloweenVN.Dialogue
{
    public class DialogueManager : MonoBehaviour
    {
        public static DialogueManager Instance { get; private set; }

        public event Action OnDialogueStarted;
        public event Action OnDialogueEnded;
        public event Action<DialogueNode> OnNodeDisplayed;
        public event Action<List<DialogueChoice>> OnChoicesDisplayed;

        public bool IsPlaying { get; private set; }

        private DialogueContainer currentDialogue;
        private DialogueNode currentNode;
        private bool isTyping;
        private Coroutine typingCoroutine;

        private void Awake()
        {
            if (Instance == null)
            {
                Instance = this;
                DontDestroyOnLoad(gameObject);
            }
            else
            {
                Destroy(gameObject);
            }
        }

        private void OnEnable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged += HandlePhaseChanged;
            }
        }

        private void OnDisable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged -= HandlePhaseChanged;
            }
        }

        private void HandlePhaseChanged(GamePhase phase)
        {
            // Dialogues could still be played during Investigation or other phases,
            // so we don't necessarily disable completely, but we can hook in phase logic if needed.
        }

        /// <summary>
        /// Starts a dialogue loaded from the specified ID.
        /// </summary>
        /// <param name="dialogueId">The ID of the dialogue to load.</param>
        public void StartDialogue(string dialogueId)
        {
            DialogueContainer container = DataLoader.LoadDialogue(dialogueId);
            if (container != null)
            {
                StartDialogue(container);
            }
            else
            {
                Debug.LogError($"Dialogue with ID {dialogueId} not found.");
            }
        }

        /// <summary>
        /// Starts a dialogue using the provided container.
        /// </summary>
        /// <param name="container">The dialogue container.</param>
        public void StartDialogue(DialogueContainer container)
        {
            currentDialogue = container;
            IsPlaying = true;
            OnDialogueStarted?.Invoke();
            
            if (currentDialogue != null && currentDialogue.nodes != null && currentDialogue.nodes.Count > 0)
            {
                DisplayNode(currentDialogue.nodes[0].id);
            }
            else
            {
                EndDialogue();
            }
        }

        /// <summary>
        /// Displays a specific dialogue node by ID.
        /// </summary>
        /// <param name="nodeId">The node ID to display.</param>
        public void DisplayNode(int nodeId)
        {
            currentNode = FindNode(nodeId);
            if (currentNode == null)
            {
                EndDialogue();
                return;
            }

            if (!string.IsNullOrEmpty(currentNode.command))
            {
                if (currentNode.command.StartsWith("CHANGE_PHASE:"))
                {
                    string phaseString = currentNode.command.Substring("CHANGE_PHASE:".Length);
                    if (Enum.TryParse(phaseString, out GamePhase phase))
                    {
                        GameManager.Instance.ChangePhase(phase);
                    }
                    
                    if (currentNode.nextNodeId != -1)
                    {
                        DisplayNode(currentNode.nextNodeId);
                        return;
                    }
                    else
                    {
                        EndDialogue();
                        return;
                    }
                }
                else if (currentNode.command.StartsWith("START_DIALOGUE:"))
                {
                    string nextDialogueId = currentNode.command.Substring("START_DIALOGUE:".Length);
                    EndDialogue();
                    StartDialogue(nextDialogueId);
                    return;
                }
                else if (currentNode.command == "END")
                {
                    EndDialogue();
                    return;
                }
            }
            
            if (currentNode.nextNodeId == -1 && string.IsNullOrEmpty(currentNode.command) && (currentNode.choices == null || currentNode.choices.Count == 0))
            {
                // This indicates the end, but we still display the node text first.
                // AdvanceDialogue will handle the termination.
            }

            OnNodeDisplayed?.Invoke(currentNode);

            if (currentNode.choices != null && currentNode.choices.Count > 0)
            {
                OnChoicesDisplayed?.Invoke(currentNode.choices);
            }
        }

        /// <summary>
        /// Advances the dialogue to the next node, or ends it if there are no more nodes.
        /// </summary>
        public void AdvanceDialogue()
        {
            if (currentNode == null || !IsPlaying) return;

            // Note: If UI is typing, skip to end is handled by DialogueUI. 
            // Here, we handle the case where we're not typing and there are no choices.

            if (currentNode.choices != null && currentNode.choices.Count > 0)
            {
                // Cannot advance by click if choices are present.
                return;
            }

            if (currentNode.nextNodeId != -1)
            {
                DisplayNode(currentNode.nextNodeId);
            }
            else
            {
                EndDialogue();
            }
        }

        /// <summary>
        /// Selects a dialogue choice and proceeds to its target node.
        /// </summary>
        /// <param name="choiceIndex">The index of the choice selected.</param>
        public void SelectChoice(int choiceIndex)
        {
            if (currentNode != null && currentNode.choices != null && choiceIndex >= 0 && choiceIndex < currentNode.choices.Count)
            {
                int nextId = currentNode.choices[choiceIndex].nextNodeId;
                if (nextId != -1)
                {
                    DisplayNode(nextId);
                }
                else
                {
                    EndDialogue();
                }
            }
        }

        /// <summary>
        /// Ends the current dialogue.
        /// </summary>
        public void EndDialogue()
        {
            IsPlaying = false;
            currentDialogue = null;
            currentNode = null;
            OnDialogueEnded?.Invoke();
        }

        private DialogueNode FindNode(int nodeId)
        {
            if (currentDialogue != null && currentDialogue.nodes != null)
            {
                return currentDialogue.nodes.Find(n => n.id == nodeId);
            }
            return null;
        }
    }
}
