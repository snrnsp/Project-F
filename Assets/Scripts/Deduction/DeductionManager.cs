using HalloweenVN.Core;
using HalloweenVN.Data;
using HalloweenVN.Investigation;
using HalloweenVN.Dialogue;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace HalloweenVN.Deduction
{
    [System.Serializable]
    public class DeductionResult
    {
        public int totalQuestions;
        public int correctAnswers;
        public bool isPerfect;
        public List<bool> questionResults;
    }

    /// <summary>
    /// Manages the deduction phase logic, handling case loading, evidence assignment, and submission.
    /// </summary>
    public class DeductionManager : MonoBehaviour
    {
        [SerializeField] private string currentCaseId = "ch1_case";
        
        private CaseContainer currentCase;
        private Dictionary<int, string> slotAssignments = new Dictionary<int, string>();
        
        /// <summary>
        /// Triggered when a new case is successfully loaded.
        /// </summary>
        public event Action<CaseContainer> OnCaseLoaded;
        
        /// <summary>
        /// Triggered when the player submits their deduction, providing the results.
        /// </summary>
        public event Action<DeductionResult> OnDeductionComplete;

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
            if (phase == GamePhase.Deduction)
            {
                LoadCase(currentCaseId);
            }
        }

        /// <summary>
        /// Loads the specified case data and initializes deduction slots.
        /// </summary>
        /// <param name="caseId">The ID of the case to load.</param>
        public void LoadCase(string caseId)
        {
            currentCase = DataLoader.LoadCase(caseId);
            slotAssignments.Clear();
            
            if (currentCase != null)
            {
                for (int i = 0; i < currentCase.questions.Count; i++)
                {
                    slotAssignments[i] = string.Empty;
                }
                OnCaseLoaded?.Invoke(currentCase);
            }
            else
            {
                Debug.LogError($"Failed to load case: {caseId}");
            }
        }

        /// <summary>
        /// Assigns an evidence item to a specific question slot.
        /// </summary>
        /// <param name="questionIndex">The index of the question slot.</param>
        /// <param name="evidenceId">The ID of the assigned evidence.</param>
        public void AssignEvidenceToSlot(int questionIndex, string evidenceId)
        {
            if (slotAssignments.ContainsKey(questionIndex))
            {
                slotAssignments[questionIndex] = evidenceId;
            }
        }

        /// <summary>
        /// Removes assigned evidence from a specific question slot.
        /// </summary>
        /// <param name="questionIndex">The index of the question slot.</param>
        public void RemoveEvidenceFromSlot(int questionIndex)
        {
            if (slotAssignments.ContainsKey(questionIndex))
            {
                slotAssignments[questionIndex] = string.Empty;
            }
        }

        /// <summary>
        /// Retrieves the currently assigned evidence ID for a given question slot.
        /// </summary>
        /// <param name="questionIndex">The index of the question slot.</param>
        /// <returns>The assigned evidence ID, or empty if none.</returns>
        public string GetAssignedEvidence(int questionIndex)
        {
            if (slotAssignments.TryGetValue(questionIndex, out string evidenceId))
            {
                return evidenceId;
            }
            return string.Empty;
        }

        /// <summary>
        /// Checks if all question slots have evidence assigned to them.
        /// </summary>
        /// <returns>True if all slots are assigned, false otherwise.</returns>
        public bool AllSlotsAssigned()
        {
            if (currentCase == null) return false;
            
            for (int i = 0; i < currentCase.questions.Count; i++)
            {
                if (string.IsNullOrEmpty(GetAssignedEvidence(i)))
                {
                    return false;
                }
            }
            return true;
        }

        /// <summary>
        /// Submits the current deduction, calculates the score, and handles success/fail logic.
        /// </summary>
        /// <returns>The result of the deduction.</returns>
        public DeductionResult Submit()
        {
            if (currentCase == null) return null;

            DeductionResult result = new DeductionResult
            {
                totalQuestions = currentCase.questions.Count,
                correctAnswers = 0,
                questionResults = new List<bool>()
            };

            for (int i = 0; i < currentCase.questions.Count; i++)
            {
                string assignedId = GetAssignedEvidence(i);
                string correctId = currentCase.questions[i].correctEvidenceId;
                
                bool isCorrect = !string.IsNullOrEmpty(assignedId) && assignedId == correctId;
                result.questionResults.Add(isCorrect);
                
                if (isCorrect)
                {
                    result.correctAnswers++;
                }
            }

            result.isPerfect = (result.correctAnswers == result.totalQuestions);
            
            OnDeductionComplete?.Invoke(result);

            if (DialogueManager.Instance != null)
            {
                string dialogueId;
                if (result.isPerfect)
                {
                    dialogueId = currentCase.perfectDialogueId;
                    // Listen for the result dialogue to end, then return to lobby
                    DialogueManager.Instance.OnDialogueEnded += OnResultDialogueEnded;
                }
                else
                {
                    dialogueId = currentCase.failDialogueId;
                    // Fail dialogue ends with CHANGE_PHASE:Deduction (retry)
                }

                // Switch to Dialogue phase so DialogueUI shows
                if (GameManager.Instance != null)
                {
                    GameManager.Instance.ChangePhase(GamePhase.Dialogue);
                }
                DialogueManager.Instance.StartDialogue(dialogueId);
            }

            return result;
        }

        /// <summary>
        /// Returns the currently loaded case.
        /// </summary>
        /// <returns>The active case container.</returns>
        public CaseContainer GetCurrentCase()
        {
            return currentCase;
        }

        /// <summary>
        /// Called when the result dialogue ends (perfect ending). Returns to lobby.
        /// </summary>
        private void OnResultDialogueEnded()
        {
            if (DialogueManager.Instance != null)
            {
                DialogueManager.Instance.OnDialogueEnded -= OnResultDialogueEnded;
            }
            if (GameManager.Instance != null)
            {
                GameManager.Instance.ChangePhase(GamePhase.Lobby);
            }
        }
    }
}
