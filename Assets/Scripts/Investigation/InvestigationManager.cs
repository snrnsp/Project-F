using HalloweenVN.Core;
using HalloweenVN.Data;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace HalloweenVN.Investigation
{
    public class InvestigationManager : MonoBehaviour
    {
        [SerializeField] private string evidenceDatabaseName = "ch1_evidence";
        [SerializeField] private string caseId = "ch1_case";
        [SerializeField] private List<string> requiredEvidenceIds = new List<string>();
        [SerializeField] private GameObject investigationUI;
        [SerializeField] private InvestigationObject[] investigationObjects;

        private EvidenceDatabase evidenceDatabase;

        public event Action OnAllEvidenceCollected;

        public int RequiredEvidenceCount => requiredEvidenceIds.Count;

        private void Start()
        {
            evidenceDatabase = DataLoader.LoadEvidenceDatabase(evidenceDatabaseName);
        }

        private void OnEnable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged += HandlePhaseChanged;
            }
            if (EvidenceInventory.Instance != null)
            {
                EvidenceInventory.Instance.OnEvidenceAdded += HandleEvidenceAdded;
            }
        }

        private void OnDisable()
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.OnPhaseChanged -= HandlePhaseChanged;
            }
            if (EvidenceInventory.Instance != null)
            {
                EvidenceInventory.Instance.OnEvidenceAdded -= HandleEvidenceAdded;
            }
        }

        private void HandlePhaseChanged(GamePhase phase)
        {
            bool isInvestigation = phase == GamePhase.Investigation;
            
            if (investigationUI != null)
            {
                investigationUI.SetActive(isInvestigation);
            }

            foreach (var obj in investigationObjects)
            {
                if (obj != null)
                {
                    obj.gameObject.SetActive(isInvestigation);
                }
            }
        }

        private void HandleEvidenceAdded(EvidenceInfo evidence)
        {
            if (CanProceedToDeduction())
            {
                OnAllEvidenceCollected?.Invoke();
            }
        }

        /// <summary>
        /// Checks if all required evidence has been collected to proceed.
        /// </summary>
        /// <returns>True if all required evidence is collected, otherwise false.</returns>
        public bool CanProceedToDeduction()
        {
            if (EvidenceInventory.Instance == null) return false;

            foreach (string id in requiredEvidenceIds)
            {
                if (!EvidenceInventory.Instance.HasEvidence(id))
                {
                    return false;
                }
            }
            return true;
        }

        /// <summary>
        /// Proceeds to the deduction phase.
        /// </summary>
        public void ProceedToDeduction()
        {
            if (GameManager.Instance != null && CanProceedToDeduction())
            {
                GameManager.Instance.ChangePhase(GamePhase.Deduction);
            }
        }

        /// <summary>
        /// Gets an evidence info by its ID from the database.
        /// </summary>
        /// <param name="id">The ID of the evidence.</param>
        /// <returns>The evidence info or null if not found.</returns>
        public EvidenceInfo GetEvidenceById(string id)
        {
            if (evidenceDatabase == null || evidenceDatabase.evidences == null) return null;
            return evidenceDatabase.evidences.Find(e => e.id == id);
        }
    }
}
