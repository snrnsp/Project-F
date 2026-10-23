using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using HalloweenVN.UI.Theme;

namespace HalloweenVN.UI
{
    /// <summary>
    /// Hover feedback for a clickable backlog entry: highlights the border,
    /// brightens the box and reveals the "rewind" hint.
    /// </summary>
    public class BacklogEntryHover : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
    {
        public Image background;
        public Outline outline;
        public GameObject hint;

        public Color normalBg;
        public Color hoverBg;
        public Color normalBorder;
        public Color hoverBorder = HalloweenTheme.AccentOrange;
        public bool isCurrentEntry;

        public void ResetHover()
        {
            if (background != null) background.color = normalBg;
            if (outline != null) outline.effectColor = normalBorder;
            if (hint != null) hint.SetActive(isCurrentEntry);
        }

        private void OnEnable()
        {
            if (normalBg.a > 0f || normalBorder.a > 0f)
            {
                ResetHover();
            }
        }

        public void OnPointerEnter(PointerEventData eventData)
        {
            if (!enabled || isCurrentEntry) return;
            SetHover(true);
        }

        public void OnPointerExit(PointerEventData eventData)
        {
            if (!enabled || isCurrentEntry) return;
            SetHover(false);
        }

        private void SetHover(bool on)
        {
            if (background != null) background.color = on ? hoverBg : normalBg;
            if (outline != null) outline.effectColor = on ? hoverBorder : normalBorder;
            if (hint != null) hint.SetActive(on);
        }
    }
}
