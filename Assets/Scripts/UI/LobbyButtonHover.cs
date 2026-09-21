using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;
using TMPro;
using System.Collections;

namespace HalloweenVN.UI
{
    /// <summary>
    /// Lobby button hover effect ported from old project.
    /// Smoothly transitions between normal and hover colors using Coroutines.
    /// </summary>
    public class LobbyButtonHover : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
    {
        public Color normalBgColor = new Color(60f/255f, 30f/255f, 80f/255f, 240f/255f);
        public Color hoverBgColor = new Color(200f/255f, 110f/255f, 20f/255f, 1f);

        public Color normalTextColor = new Color(255f/255f, 200f/255f, 100f/255f, 1f);
        public Color hoverTextColor = Color.white;

        private Image bgImage;
        private TextMeshProUGUI label;
        private Coroutine fadeCoroutine;
        private const float FADE_DURATION = 0.15f;

        private void Awake()
        {
            bgImage = GetComponent<Image>();
            label = GetComponentInChildren<TextMeshProUGUI>();
        }

        public void OnPointerEnter(PointerEventData eventData)
        {
            if (fadeCoroutine != null) StopCoroutine(fadeCoroutine);
            fadeCoroutine = StartCoroutine(FadeColors(hoverBgColor, hoverTextColor));
        }

        public void OnPointerExit(PointerEventData eventData)
        {
            if (fadeCoroutine != null) StopCoroutine(fadeCoroutine);
            fadeCoroutine = StartCoroutine(FadeColors(normalBgColor, normalTextColor));
        }

        private IEnumerator FadeColors(Color targetBg, Color targetText)
        {
            Color startBg = bgImage != null ? bgImage.color : normalBgColor;
            Color startText = label != null ? label.color : normalTextColor;

            float elapsed = 0f;
            while (elapsed < FADE_DURATION)
            {
                elapsed += Time.unscaledDeltaTime;
                float t = Mathf.SmoothStep(0f, 1f, elapsed / FADE_DURATION);

                if (bgImage != null) bgImage.color = Color.Lerp(startBg, targetBg, t);
                if (label != null) label.color = Color.Lerp(startText, targetText, t);
                yield return null;
            }

            if (bgImage != null) bgImage.color = targetBg;
            if (label != null) label.color = targetText;
        }
    }
}
