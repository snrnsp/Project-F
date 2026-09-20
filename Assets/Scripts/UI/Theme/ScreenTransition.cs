using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System;
using HalloweenVN.Core;

namespace HalloweenVN.UI.Theme
{
    public class ScreenTransition : MonoBehaviour
    {
        [SerializeField] private float transitionDuration = 0.5f;
        [SerializeField] private bool autoTransitionOnPhaseChange = true;
        
        private Image overlayImage;
        private bool isTransitioning;
        private Coroutine transitionCoroutine;
        private GameManager gameManager;
        
        private void Awake()
        {
            Canvas canvas = GetComponent<Canvas>();
            if (canvas == null)
            {
                canvas = gameObject.AddComponent<Canvas>();
                canvas.renderMode = RenderMode.ScreenSpaceOverlay;
                canvas.sortingOrder = 999;
            }

            overlayImage = GetComponentInChildren<Image>();
            if (overlayImage == null)
            {
                GameObject imageObj = new GameObject("OverlayImage");
                imageObj.transform.SetParent(transform, false);
                overlayImage = imageObj.AddComponent<Image>();
                
                RectTransform rt = overlayImage.GetComponent<RectTransform>();
                rt.anchorMin = Vector2.zero;
                rt.anchorMax = Vector2.one;
                rt.sizeDelta = Vector2.zero;
            }
            
            Color c = HalloweenTheme.TransitionColor;
            c.a = 0f;
            overlayImage.color = c;
            overlayImage.raycastTarget = false;
        }

        private void OnEnable()
        {
            gameManager = FindFirstObjectByType<GameManager>();
            if (gameManager != null)
            {
                gameManager.OnPhaseChanged += HandlePhaseChanged;
            }
        }

        private void OnDisable()
        {
            if (gameManager != null)
            {
                gameManager.OnPhaseChanged -= HandlePhaseChanged;
            }
        }

        private void HandlePhaseChanged(GamePhase phase)
        {
            if (autoTransitionOnPhaseChange)
            {
                TransitionFade();
            }
        }

        /// <summary>
        /// Fades the screen out to the transition color (darkens screen).
        /// </summary>
        /// <param name="duration">Duration of the fade.</param>
        /// <param name="onComplete">Callback to invoke when fading out is complete.</param>
        public void FadeOut(float duration, Action onComplete = null)
        {
            if (transitionCoroutine != null) StopCoroutine(transitionCoroutine);
            transitionCoroutine = StartCoroutine(FadeCoroutine(0f, 1f, duration, HalloweenTheme.TransitionColor, onComplete));
        }

        /// <summary>
        /// Fades the screen in from the transition color (reveals screen).
        /// </summary>
        /// <param name="duration">Duration of the fade.</param>
        /// <param name="onComplete">Callback to invoke when fading in is complete.</param>
        public void FadeIn(float duration, Action onComplete = null)
        {
            if (transitionCoroutine != null) StopCoroutine(transitionCoroutine);
            transitionCoroutine = StartCoroutine(FadeCoroutine(1f, 0f, duration, HalloweenTheme.TransitionColor, onComplete));
        }

        /// <summary>
        /// Performs a full fade out and fade in transition.
        /// </summary>
        /// <param name="onMidpoint">Callback invoked when the screen is fully faded out, before fading back in.</param>
        public void TransitionFade(Action onMidpoint = null)
        {
            if (isTransitioning) return;
            if (transitionCoroutine != null) StopCoroutine(transitionCoroutine);
            transitionCoroutine = StartCoroutine(FullTransitionCoroutine(transitionDuration, HalloweenTheme.TransitionColor, onMidpoint));
        }

        /// <summary>
        /// Flashes the screen red, useful for wrong answers or damage.
        /// </summary>
        /// <param name="duration">Total duration of the flash.</param>
        public void FlashRed(float duration = 0.3f)
        {
            if (transitionCoroutine != null) StopCoroutine(transitionCoroutine);
            transitionCoroutine = StartCoroutine(FullTransitionCoroutine(duration, Color.red, null));
        }

        /// <summary>
        /// Flashes the screen white, useful for dramatic moments or success.
        /// </summary>
        /// <param name="duration">Total duration of the flash.</param>
        public void FlashWhite(float duration = 0.3f)
        {
            if (transitionCoroutine != null) StopCoroutine(transitionCoroutine);
            transitionCoroutine = StartCoroutine(FullTransitionCoroutine(duration, Color.white, null));
        }

        private IEnumerator FadeCoroutine(float startAlpha, float endAlpha, float duration, Color color, Action onComplete)
        {
            isTransitioning = true;
            overlayImage.raycastTarget = true;
            
            color.a = startAlpha;
            overlayImage.color = color;
            
            float time = 0f;
            while (time < duration)
            {
                time += Time.deltaTime;
                float t = Mathf.Clamp01(time / duration);
                float smoothT = Mathf.SmoothStep(0f, 1f, t);
                
                color.a = Mathf.Lerp(startAlpha, endAlpha, smoothT);
                overlayImage.color = color;
                
                yield return null;
            }
            
            color.a = endAlpha;
            overlayImage.color = color;
            
            if (endAlpha == 0f)
            {
                overlayImage.raycastTarget = false;
            }
            
            isTransitioning = false;
            onComplete?.Invoke();
        }

        private IEnumerator FullTransitionCoroutine(float duration, Color color, Action onMidpoint)
        {
            isTransitioning = true;
            overlayImage.raycastTarget = true;
            
            float halfDuration = duration * 0.5f;
            
            // Fade Out
            float time = 0f;
            while (time < halfDuration)
            {
                time += Time.deltaTime;
                float t = Mathf.Clamp01(time / halfDuration);
                color.a = Mathf.SmoothStep(0f, 1f, t);
                overlayImage.color = color;
                yield return null;
            }
            color.a = 1f;
            overlayImage.color = color;
            
            onMidpoint?.Invoke();
            
            // Fade In
            time = 0f;
            while (time < halfDuration)
            {
                time += Time.deltaTime;
                float t = Mathf.Clamp01(time / halfDuration);
                color.a = Mathf.Lerp(1f, 0f, Mathf.SmoothStep(0f, 1f, t));
                overlayImage.color = color;
                yield return null;
            }
            color.a = 0f;
            overlayImage.color = color;
            
            overlayImage.raycastTarget = false;
            isTransitioning = false;
        }
    }
}
