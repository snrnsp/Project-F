using UnityEngine;
using UnityEngine.InputSystem;

namespace HalloweenVN.UI
{
    /// <summary>
    /// Applies a subtle parallax movement to the UI element based on mouse position.
    /// Used for the Lobby background to give it a dynamic feel.
    /// </summary>
    public class UIMouseParallax : MonoBehaviour
    {
        [Tooltip("Maximum pixels the image can move from its center")]
        public float movementOffset = 25f;
        
        [Tooltip("How fast the image lerps to the target position")]
        public float smoothSpeed = 4f;

        private RectTransform _rectTransform;
        private Vector2 _startPosition;

        private void Awake()
        {
            _rectTransform = GetComponent<RectTransform>();
            _startPosition = _rectTransform.anchoredPosition;
        }

        private void Update()
        {
            if (Mouse.current == null) return;
            
            Vector2 mousePos = Mouse.current.position.ReadValue();
            
            // Normalize mouse position relative to screen center (-1 to 1)
            float normX = (mousePos.x / Screen.width) * 2f - 1f;
            float normY = (mousePos.y / Screen.height) * 2f - 1f;

            // Calculate target position (inverted so background moves opposite to mouse for depth)
            Vector2 targetPos = _startPosition + new Vector2(normX * -movementOffset, normY * -movementOffset);

            // Lerp towards the target position only when noticeably different to avoid dirtying Canvas every idle frame
            Vector2 currentPos = _rectTransform.anchoredPosition;
            if ((targetPos - currentPos).sqrMagnitude > 0.0004f)
            {
                _rectTransform.anchoredPosition = Vector2.Lerp(currentPos, targetPos, Time.unscaledDeltaTime * smoothSpeed);
            }
        }
    }
}
