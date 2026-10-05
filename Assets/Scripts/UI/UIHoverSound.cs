using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

namespace HalloweenVN.UI
{
    public class UIHoverSound : MonoBehaviour, IPointerEnterHandler, IPointerClickHandler
    {
        public string hoverSoundName = "sfx_ui_hover";
        public string clickSoundName = "sfx_ui_click";

        public void OnPointerEnter(PointerEventData eventData)
        {
            if (Core.AudioManager.Instance != null)
            {
                Core.AudioManager.Instance.PlaySFX(hoverSoundName);
            }
        }

        public void OnPointerClick(PointerEventData eventData)
        {
            if (Core.AudioManager.Instance != null)
            {
                Core.AudioManager.Instance.PlaySFX(clickSoundName);
            }
        }
    }
}
