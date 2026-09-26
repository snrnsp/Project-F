using HalloweenVN.Data;
using HalloweenVN.Dialogue;
using HalloweenVN.Core;
using UnityEngine;

namespace HalloweenVN.Investigation
{
    [RequireComponent(typeof(Collider2D))]
    public class InvestigationObject : MonoBehaviour
    {
        [SerializeField] private string evidenceId;
        [SerializeField] private string investigationDialogueId;
        [SerializeField] private SpriteRenderer highlightRenderer;
        [SerializeField] private bool isCollected = false;

        private EvidenceInfo cachedEvidence;

        private void Start()
        {
            InvestigationManager manager = FindAnyObjectByType<InvestigationManager>();
            if (manager != null && !string.IsNullOrEmpty(evidenceId))
            {
                cachedEvidence = manager.GetEvidenceById(evidenceId);
            }
        }

        private void OnMouseDown()
        {
            if (isCollected) return;

            if (GameManager.Instance != null && GameManager.Instance.CurrentPhase == GamePhase.Investigation)
            {
                isCollected = true;
                
                if (cachedEvidence != null && EvidenceInventory.Instance != null)
                {
                    EvidenceInventory.Instance.AddEvidence(cachedEvidence);
                }

                if (DialogueManager.Instance != null && !string.IsNullOrEmpty(investigationDialogueId))
                {
                    DialogueManager.Instance.StartDialogue(investigationDialogueId);
                }

                if (highlightRenderer != null)
                {
                    highlightRenderer.enabled = false;
                }
            }
        }

        /// <summary>
        /// Initializes the investigation object with evidence from code.
        /// </summary>
        /// <param name="evidence">The evidence to initialize with.</param>
        public void Initialize(EvidenceInfo evidence)
        {
            cachedEvidence = evidence;
            if (evidence != null)
            {
                evidenceId = evidence.id;
            }
        }

        /// <summary>
        /// Checks if the object has already been collected.
        /// </summary>
        public bool IsCollected => isCollected;
    }
}
