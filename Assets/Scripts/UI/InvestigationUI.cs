using HalloweenVN.Investigation;
using HalloweenVN.Data;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

namespace HalloweenVN.UI
{
    public class InvestigationUI : MonoBehaviour
    {
        [SerializeField] private GameObject evidenceListPanel;
        [SerializeField] private Transform evidenceListContainer;
        [SerializeField] private GameObject evidenceItemPrefab;
        [SerializeField] private Button proceedButton;
        [SerializeField] private TextMeshProUGUI evidenceCountText;
        [SerializeField] private GameObject evidenceDetailPanel;
        [SerializeField] private TextMeshProUGUI evidenceDetailName;
        [SerializeField] private TextMeshProUGUI evidenceDetailDescription;
        [SerializeField] private Image evidenceDetailIcon;

        private InvestigationManager investigationManager;

        private void Awake()
        {
            investigationManager = FindAnyObjectByType<InvestigationManager>();
        }

        private void OnEnable()
        {
            if (EvidenceInventory.Instance != null)
            {
                EvidenceInventory.Instance.OnEvidenceAdded += OnEvidenceAddedHandler;
            }
            if (investigationManager != null)
            {
                investigationManager.OnAllEvidenceCollected += EnableProceedButton;
            }
            
            if (proceedButton != null)
            {
                proceedButton.onClick.AddListener(OnProceedClicked);
                proceedButton.interactable = false;
            }

            RefreshEvidenceList();
        }

        private void OnDisable()
        {
            if (EvidenceInventory.Instance != null)
            {
                EvidenceInventory.Instance.OnEvidenceAdded -= OnEvidenceAddedHandler;
            }
            if (investigationManager != null)
            {
                investigationManager.OnAllEvidenceCollected -= EnableProceedButton;
            }
            
            if (proceedButton != null)
            {
                proceedButton.onClick.RemoveListener(OnProceedClicked);
            }
        }

        private void OnEvidenceAddedHandler(EvidenceInfo evidence)
        {
            AddEvidenceItem(evidence);
            int requiredCount = investigationManager != null ? investigationManager.RequiredEvidenceCount : 0;
            UpdateEvidenceCount(EvidenceInventory.Instance.Count, requiredCount);
        }

        /// <summary>
        /// Clears and rebuilds the evidence list from the inventory.
        /// </summary>
        public void RefreshEvidenceList()
        {
            if (evidenceListContainer == null) return;
            
            foreach (Transform child in evidenceListContainer)
            {
                Destroy(child.gameObject);
            }

            if (EvidenceInventory.Instance != null)
            {
                List<EvidenceInfo> allEvidence = EvidenceInventory.Instance.GetAllEvidence();
                foreach (var evidence in allEvidence)
                {
                    AddEvidenceItem(evidence);
                }
                
                int requiredCount = investigationManager != null ? investigationManager.RequiredEvidenceCount : 0;
                UpdateEvidenceCount(allEvidence.Count, requiredCount);
            }
        }

        /// <summary>
        /// Adds a single evidence item to the list UI.
        /// </summary>
        /// <param name="evidence">The evidence to add.</param>
        public void AddEvidenceItem(EvidenceInfo evidence)
        {
            if (evidenceItemPrefab == null || evidenceListContainer == null) return;
            
            GameObject itemObj = Instantiate(evidenceItemPrefab, evidenceListContainer);
            TextMeshProUGUI itemText = itemObj.GetComponentInChildren<TextMeshProUGUI>();
            if (itemText != null)
            {
                itemText.text = evidence.evidenceName;
            }
            
            Button itemBtn = itemObj.GetComponent<Button>();
            if (itemBtn != null)
            {
                itemBtn.onClick.AddListener(() => ShowEvidenceDetail(evidence));
            }
        }

        /// <summary>
        /// Shows the evidence detail popup.
        /// </summary>
        /// <param name="evidence">The evidence to show details for.</param>
        public void ShowEvidenceDetail(EvidenceInfo evidence)
        {
            if (evidenceDetailPanel != null) evidenceDetailPanel.SetActive(true);
            if (evidenceDetailName != null) evidenceDetailName.text = evidence.evidenceName;
            if (evidenceDetailDescription != null) evidenceDetailDescription.text = evidence.description;
            if (evidenceDetailIcon != null && !string.IsNullOrEmpty(evidence.iconPath))
            {
                Sprite icon = Resources.Load<Sprite>(evidence.iconPath);
                if (icon != null)
                {
                    evidenceDetailIcon.sprite = icon;
                }
            }
        }

        /// <summary>
        /// Hides the evidence detail popup.
        /// </summary>
        public void HideEvidenceDetail()
        {
            if (evidenceDetailPanel != null) evidenceDetailPanel.SetActive(false);
        }

        /// <summary>
        /// Updates the evidence count text.
        /// </summary>
        /// <param name="current">Current number of collected evidence.</param>
        /// <param name="required">Required number of evidence.</param>
        public void UpdateEvidenceCount(int current, int required)
        {
            if (evidenceCountText != null)
            {
                evidenceCountText.text = $"수집한 증거: {current}/{required}";
            }
        }

        /// <summary>
        /// Called when the proceed button is clicked.
        /// </summary>
        public void OnProceedClicked()
        {
            if (investigationManager != null)
            {
                investigationManager.ProceedToDeduction();
            }
        }

        /// <summary>
        /// Enables the proceed button.
        /// </summary>
        public void EnableProceedButton()
        {
            if (proceedButton != null)
            {
                proceedButton.interactable = true;
            }
        }
    }
}
