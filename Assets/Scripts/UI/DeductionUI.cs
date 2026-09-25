using HalloweenVN.Deduction;
using HalloweenVN.Data;
using HalloweenVN.Investigation;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

namespace HalloweenVN.UI
{
    /// <summary>
    /// Handles the UI for the deduction phase, displaying questions and available evidence.
    /// </summary>
    public class DeductionUI : MonoBehaviour
    {
        [SerializeField] private GameObject deductionPanel;
        [SerializeField] private Transform questionContainer;
        [SerializeField] private GameObject questionSlotPrefab;
        [SerializeField] private Transform evidenceInventoryContainer;
        [SerializeField] private GameObject evidenceDragItemPrefab;
        [SerializeField] private Button submitButton;
        [SerializeField] private TextMeshProUGUI caseNameText;
        [SerializeField] private GameObject resultPanel;
        [SerializeField] private TextMeshProUGUI resultText;
        [SerializeField] private Button resultProceedButton;
        
        private DeductionManager deductionManager;
        private List<EvidenceSlot> currentSlots = new List<EvidenceSlot>();

        private void Awake()
        {
            deductionManager = FindFirstObjectByType<DeductionManager>();
            if (submitButton != null)
            {
                submitButton.onClick.AddListener(OnSubmitClicked);
            }
            if (resultProceedButton != null)
            {
                resultProceedButton.onClick.AddListener(OnResultProceedClicked);
            }
        }

        private void OnResultProceedClicked()
        {
            if (resultPanel != null)
            {
                resultPanel.SetActive(false);
            }
            Hide();
        }

        private void OnEnable()
        {
            if (deductionManager != null)
            {
                deductionManager.OnCaseLoaded += SetupCase;
                deductionManager.OnDeductionComplete += ShowResult;
            }
        }

        private void OnDisable()
        {
            if (deductionManager != null)
            {
                deductionManager.OnCaseLoaded -= SetupCase;
                deductionManager.OnDeductionComplete -= ShowResult;
            }
        }

        /// <summary>
        /// Sets up the UI for the loaded case, creating slots and evidence items.
        /// </summary>
        /// <param name="caseData">The case data to display.</param>
        public void SetupCase(CaseContainer caseData)
        {
            Show();
            ClearUI();
            
            if (caseNameText != null)
            {
                caseNameText.text = caseData.caseName;
            }
            
            // Build question slots
            for (int i = 0; i < caseData.questions.Count; i++)
            {
                GameObject slotObj = Instantiate(questionSlotPrefab, questionContainer);
                EvidenceSlot slot = slotObj.GetComponent<EvidenceSlot>();
                if (slot != null)
                {
                    slot.Initialize(i, caseData.questions[i].questionText, deductionManager);
                    currentSlots.Add(slot);
                }
            }
            
            // Build evidence inventory
            if (EvidenceInventory.Instance != null)
            {
                List<EvidenceInfo> allEvidence = EvidenceInventory.Instance.GetAllEvidence();
                if (allEvidence != null)
                {
                    foreach (var evidence in allEvidence)
                    {
                        GameObject dragObj = Instantiate(evidenceDragItemPrefab, evidenceInventoryContainer);
                        EvidenceDragItem dragItem = dragObj.GetComponent<EvidenceDragItem>();
                        if (dragItem != null)
                        {
                            dragItem.Initialize(evidence);
                        }
                    }
                }
            }
            
            RefreshSubmitButton();
        }

        private void Update()
        {
            RefreshSubmitButton();
        }

        /// <summary>
        /// Enables the submit button if all slots are filled.
        /// </summary>
        public void RefreshSubmitButton()
        {
            if (submitButton != null && deductionManager != null)
            {
                submitButton.interactable = deductionManager.AllSlotsAssigned();
            }
        }

        /// <summary>
        /// Handles the submit button click event.
        /// </summary>
        public void OnSubmitClicked()
        {
            if (deductionManager != null)
            {
                deductionManager.Submit();
            }
        }

        /// <summary>
        /// Displays the deduction result panel.
        /// </summary>
        /// <param name="result">The result to display.</param>
        public void ShowResult(DeductionResult result)
        {
            if (resultPanel != null)
            {
                resultPanel.SetActive(true);
            }
            if (resultText != null)
            {
                resultText.text = $"결과: {result.correctAnswers} / {result.totalQuestions}";
                if (result.isPerfect)
                {
                    resultText.text += "\n완벽한 추리!";
                }
            }
        }

        /// <summary>
        /// Shows the deduction UI panel.
        /// </summary>
        public void Show()
        {
            if (deductionPanel != null)
            {
                deductionPanel.SetActive(true);
            }
            if (resultPanel != null)
            {
                resultPanel.SetActive(false);
            }
        }

        /// <summary>
        /// Hides the deduction UI panel.
        /// </summary>
        public void Hide()
        {
            if (deductionPanel != null)
            {
                deductionPanel.SetActive(false);
            }
        }

        /// <summary>
        /// Clears all generated UI elements from the container.
        /// </summary>
        public void ClearUI()
        {
            foreach (Transform child in questionContainer)
            {
                Destroy(child.gameObject);
            }
            foreach (Transform child in evidenceInventoryContainer)
            {
                Destroy(child.gameObject);
            }
            currentSlots.Clear();
        }
    }
}
