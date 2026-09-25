using HalloweenVN.Data;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

namespace HalloweenVN.UI
{
    /// <summary>
    /// Handles the dragging behavior for evidence items in the UI.
    /// </summary>
    public class EvidenceDragItem : MonoBehaviour, IBeginDragHandler, IDragHandler, IEndDragHandler
    {
        [SerializeField] private Image iconImage;
        [SerializeField] private TextMeshProUGUI nameText;
        
        private EvidenceInfo evidenceInfo;
        private Canvas canvas;
        private RectTransform rectTransform;
        private CanvasGroup canvasGroup;
        private Vector3 originalPosition;
        private Transform originalParent;

        private void Awake()
        {
            rectTransform = GetComponent<RectTransform>();
            canvasGroup = GetComponent<CanvasGroup>();
            if (canvasGroup == null)
            {
                canvasGroup = gameObject.AddComponent<CanvasGroup>();
            }
            canvas = GetComponentInParent<Canvas>();
        }

        /// <summary>
        /// Initializes the drag item with evidence data.
        /// </summary>
        /// <param name="evidence">The evidence info.</param>
        public void Initialize(EvidenceInfo evidence)
        {
            evidenceInfo = evidence;
            if (nameText != null)
            {
                nameText.text = evidence.evidenceName;
            }
            if (iconImage != null && !string.IsNullOrEmpty(evidence.iconPath))
            {
                Sprite iconSprite = Resources.Load<Sprite>(evidence.iconPath);
                if (iconSprite != null)
                {
                    iconImage.sprite = iconSprite;
                }
            }
        }

        /// <summary>
        /// Retrieves the evidence info associated with this item.
        /// </summary>
        /// <returns>The evidence info.</returns>
        public EvidenceInfo GetEvidenceInfo()
        {
            return evidenceInfo;
        }

        /// <summary>
        /// Called when the user begins dragging the item.
        /// </summary>
        /// <param name="eventData">Pointer event data.</param>
        public void OnBeginDrag(PointerEventData eventData)
        {
            originalPosition = rectTransform.anchoredPosition;
            originalParent = transform.parent;
            
            if (canvasGroup != null)
            {
                canvasGroup.blocksRaycasts = false;
            }
            
            if (canvas != null)
            {
                transform.SetParent(canvas.transform);
                transform.SetAsLastSibling();
            }
        }

        /// <summary>
        /// Called while the user is dragging the item.
        /// </summary>
        /// <param name="eventData">Pointer event data.</param>
        public void OnDrag(PointerEventData eventData)
        {
            if (canvas != null)
            {
                rectTransform.anchoredPosition += eventData.delta / canvas.scaleFactor;
            }
        }

        /// <summary>
        /// Called when the user stops dragging the item.
        /// </summary>
        /// <param name="eventData">Pointer event data.</param>
        public void OnEndDrag(PointerEventData eventData)
        {
            if (canvasGroup != null)
            {
                canvasGroup.blocksRaycasts = true;
            }
            
            transform.SetParent(originalParent);
            rectTransform.anchoredPosition = originalPosition;
        }
    }
}
