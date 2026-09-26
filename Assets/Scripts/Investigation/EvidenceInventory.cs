using HalloweenVN.Data;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace HalloweenVN.Investigation
{
    public class EvidenceInventory : MonoBehaviour
    {
        public static EvidenceInventory Instance { get; private set; }

        private List<EvidenceInfo> collectedEvidence = new List<EvidenceInfo>();

        public event Action<EvidenceInfo> OnEvidenceAdded;
        public event Action OnInventoryCleared;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }

        /// <summary>
        /// Adds an evidence to the inventory if not already collected.
        /// </summary>
        /// <param name="evidence">The evidence to add.</param>
        public void AddEvidence(EvidenceInfo evidence)
        {
            if (!HasEvidence(evidence.id))
            {
                collectedEvidence.Add(evidence);
                OnEvidenceAdded?.Invoke(evidence);
            }
        }

        /// <summary>
        /// Checks if an evidence with the given id is already collected.
        /// </summary>
        /// <param name="evidenceId">The ID of the evidence.</param>
        /// <returns>True if collected, false otherwise.</returns>
        public bool HasEvidence(string evidenceId)
        {
            return collectedEvidence.Exists(e => e.id == evidenceId);
        }

        /// <summary>
        /// Gets a copy of all collected evidence.
        /// </summary>
        /// <returns>List of collected evidence.</returns>
        public List<EvidenceInfo> GetAllEvidence()
        {
            return new List<EvidenceInfo>(collectedEvidence);
        }

        /// <summary>
        /// Gets the number of collected evidence items.
        /// </summary>
        public int Count => collectedEvidence.Count;

        /// <summary>
        /// Clears all collected evidence from the inventory.
        /// </summary>
        public void Clear()
        {
            collectedEvidence.Clear();
            OnInventoryCleared?.Invoke();
        }

        /// <summary>
        /// Gets a list of collected evidence IDs for saving.
        /// </summary>
        /// <returns>List of evidence IDs.</returns>
        public List<string> GetCollectedIds()
        {
            List<string> ids = new List<string>();
            foreach (var e in collectedEvidence)
            {
                ids.Add(e.id);
            }
            return ids;
        }

        /// <summary>
        /// Restores evidence from save data by matching IDs to database entries.
        /// </summary>
        /// <param name="ids">List of saved IDs.</param>
        /// <param name="db">The evidence database.</param>
        public void RestoreFromIds(List<string> ids, EvidenceDatabase db)
        {
            Clear();
            foreach (string id in ids)
            {
                EvidenceInfo info = db.evidences.Find(e => e.id == id);
                if (info != null)
                {
                    collectedEvidence.Add(info);
                }
            }
        }
    }
}
