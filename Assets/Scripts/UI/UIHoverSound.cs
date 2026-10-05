using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

namespace HalloweenVN.UI
{
    public class UIHoverSound : MonoBehaviour, IPointerEnterHandler
    {
        public string hoverSoundName = "sfx_ui_hover";

        public void OnPointerEnter(PointerEventData eventData)
        {
            if (Core.AudioManager.Instance != null)
            {
                Core.AudioManager.Instance.PlaySFX(hoverSoundName);
            }
        }
    }
}
