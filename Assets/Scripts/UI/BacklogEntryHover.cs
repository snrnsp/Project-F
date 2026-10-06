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

        private void OnEnable() => SetHover(false);

        public void OnPointerEnter(PointerEventData eventData) => SetHover(true);
        public void OnPointerExit(PointerEventData eventData) => SetHover(false);

        private void SetHover(bool on)
        {
            if (background != null) background.color = on ? hoverBg : normalBg;
            if (outline != null) outline.effectColor = on ? hoverBorder : normalBorder;
            if (hint != null) hint.SetActive(on);
        }
    }
}
