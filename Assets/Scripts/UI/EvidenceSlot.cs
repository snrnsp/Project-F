using HalloweenVN.Deduction;
using HalloweenVN.Data;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

namespace HalloweenVN.UI
{
    /// <summary>
    /// Represents a question slot where evidence can be dropped.
    /// </summary>
    public class EvidenceSlot : MonoBehaviour, IDropHandler, IPointerClickHandler
    {
        [SerializeField] private Image slotIcon;
        [SerializeField] private TextMeshProUGUI questionText;
        [SerializeField] private Image slotBackground;
        [SerializeField] private Color emptyColor = new Color(0.3f, 0.3f, 0.3f, 0.5f);
        [SerializeField] private Color filledColor = new Color(0.5f, 0.8f, 0.5f, 0.5f);
        
        private int questionIndex;
        private string assignedEvidenceId;
        private DeductionManager deductionManager;

        /// <summary>
        /// Indicates if evidence has been assigned to this slot.
        /// </summary>
        public bool IsAssigned => !string.IsNullOrEmpty(assignedEvidenceId);

        /// <summary>
        /// Initializes the evidence slot with question details.
        /// </summary>
        /// <param name="index">The question index.</param>
        /// <param name="question">The question text.</param>
        /// <param name="manager">Reference to the DeductionManager.</param>
        public void Initialize(int index, string question, DeductionManager manager)
        {
            questionIndex = index;
            if (questionText != null)
            {
                questionText.text = question;
            }
            deductionManager = manager;
            
            ClearSlot();
        }

        /// <summary>
        /// Handles the drop event when a drag item is released over this slot.
        /// </summary>
        /// <param name="eventData">Pointer event data.</param>
        public void OnDrop(PointerEventData eventData)
        {
            if (eventData.pointerDrag != null)
            {
                EvidenceDragItem dragItem = eventData.pointerDrag.GetComponent<EvidenceDragItem>();
                if (dragItem != null)
                {
                    EvidenceInfo evidence = dragItem.GetEvidenceInfo();
                    if (evidence != null && deductionManager != null)
                    {
                        deductionManager.AssignEvidenceToSlot(questionIndex, evidence.id);
                        assignedEvidenceId = evidence.id;
                        
                        if (slotIcon != null)
                        {
                            Image draggedImage = dragItem.GetComponentInChildren<Image>();
                            if (draggedImage != null)
                            {
                                slotIcon.sprite = draggedImage.sprite;
                                slotIcon.enabled = true;
                            }
                        }
                        
                        if (slotBackground != null)
                        {
                            slotBackground.color = filledColor;
                        }
                    }
                }
            }
        }

        /// <summary>
        /// Clears the currently assigned evidence from this slot.
        /// </summary>
        public void ClearSlot()
        {
            assignedEvidenceId = string.Empty;
            
            if (deductionManager != null)
            {
                deductionManager.RemoveEvidenceFromSlot(questionIndex);
            }
            
            if (slotIcon != null)
            {
                slotIcon.sprite = null;
                slotIcon.enabled = false;
            }
            
            if (slotBackground != null)
            {
                slotBackground.color = emptyColor;
            }
        }

        /// <summary>
        /// Listens for right-click or secondary click to clear the slot.
        /// </summary>
        /// <param name="eventData">Pointer event data.</param>
        public void OnPointerClick(PointerEventData eventData)
        {
            if (eventData.button == PointerEventData.InputButton.Right)
            {
                ClearSlot();
            }
        }
    }
}
