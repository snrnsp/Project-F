using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

namespace HalloweenVN.UI
{
    /// <summary>
    /// Plays the UI hover / click sounds for a clickable element.
    /// Full-screen click areas (dialogue background, modal overlays) should set playHover = false,
    /// otherwise the hover tick fires every time the cursor crosses them.
    /// </summary>
    public class UIHoverSound : MonoBehaviour, IPointerEnterHandler, IPointerClickHandler
    {
        public string hoverSoundName = "sfx_ui_hover";
        public string clickSoundName = "sfx_ui_click";
        public bool playHover = true;
        public bool playClick = true;

        // Global throttle so sweeping the cursor across a column of buttons doesn't machine-gun the tick.
        private static float lastHoverTime = -1f;
        private const float HoverCooldown = 0.06f;

        private Selectable selectable;

        private void Awake()
        {
            selectable = GetComponent<Selectable>();
        }

        private bool IsInteractable()
        {
            return selectable == null || selectable.IsInteractable();
        }

        public void OnPointerEnter(PointerEventData eventData)
        {
            if (!playHover || !IsInteractable()) return;
            if (Time.unscaledTime - lastHoverTime < HoverCooldown) return;
            lastHoverTime = Time.unscaledTime;

            if (Core.AudioManager.Instance != null)
                Core.AudioManager.Instance.PlaySFX(hoverSoundName);
        }

        public void OnPointerClick(PointerEventData eventData)
        {
            if (!playClick || !IsInteractable()) return;
            if (eventData != null && eventData.button != PointerEventData.InputButton.Left) return;

            if (Core.AudioManager.Instance != null)
                Core.AudioManager.Instance.PlaySFX(clickSoundName);
        }
    }
}
