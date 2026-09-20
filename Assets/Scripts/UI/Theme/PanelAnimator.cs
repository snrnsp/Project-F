using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System;

namespace HalloweenVN.UI.Theme
{
    public enum AnimationType
    {
        Fade,
        SlideUp,
        SlideDown,
        SlideLeft,
        SlideRight,
        FadeAndSlideUp
    }

    [RequireComponent(typeof(CanvasGroup))]
    public class PanelAnimator : MonoBehaviour
    {
        [SerializeField] private float fadeDuration = 0.3f;
        [SerializeField] private float slideDuration = 0.4f;
        [SerializeField] private AnimationType animationType = AnimationType.Fade;
        [SerializeField] private float slideOffset = 100f;

        private CanvasGroup canvasGroup;
        private RectTransform rectTransform;
        private Vector2 originalPosition;
        private Coroutine currentAnimation;

        public bool IsAnimating { get; private set; }

        public event Action OnShowComplete;
        public event Action OnHideComplete;

        private void Awake()
        {
            canvasGroup = GetComponent<CanvasGroup>();
            if (canvasGroup == null)
            {
                canvasGroup = gameObject.AddComponent<CanvasGroup>();
            }
            rectTransform = GetComponent<RectTransform>();
            if (rectTransform != null)
            {
                originalPosition = rectTransform.anchoredPosition;
            }
        }

        /// <summary>
        /// Animates the panel appearing based on the configured animation type.
        /// </summary>
        public void ShowPanel()
        {
            if (IsAnimating) return;
            gameObject.SetActive(true);
            
            if (currentAnimation != null)
                StopCoroutine(currentAnimation);
            
            currentAnimation = StartCoroutine(ShowCoroutine());
        }

        /// <summary>
        /// Reverses the animation and hides the panel, calling the optional onComplete action when finished.
        /// </summary>
        /// <param name="onComplete">Callback to invoke after hiding is complete.</param>
        public void HidePanel(Action onComplete = null)
        {
            if (IsAnimating) return;
            
            if (currentAnimation != null)
                StopCoroutine(currentAnimation);
            
            currentAnimation = StartCoroutine(HideCoroutine(onComplete));
        }

        /// <summary>
        /// Instantly shows the panel without animation.
        /// </summary>
        public void ShowImmediate()
        {
            if (currentAnimation != null)
            {
                StopCoroutine(currentAnimation);
                currentAnimation = null;
            }
            IsAnimating = false;
            gameObject.SetActive(true);
            canvasGroup.alpha = 1f;
            if (rectTransform != null)
                rectTransform.anchoredPosition = originalPosition;
        }

        /// <summary>
        /// Instantly hides the panel without animation.
        /// </summary>
        public void HideImmediate()
        {
            if (currentAnimation != null)
            {
                StopCoroutine(currentAnimation);
                currentAnimation = null;
            }
            IsAnimating = false;
            canvasGroup.alpha = 0f;
            gameObject.SetActive(false);
        }

        private IEnumerator ShowCoroutine()
        {
            IsAnimating = true;
            float time = 0f;
            float alphaStart = 0f;
            float alphaEnd = 1f;
            Vector2 startPos = GetSlideStartPosition();
            Vector2 endPos = originalPosition;

            if (animationType == AnimationType.Fade || animationType == AnimationType.FadeAndSlideUp)
            {
                canvasGroup.alpha = alphaStart;
            }
            if (animationType != AnimationType.Fade && rectTransform != null)
            {
                rectTransform.anchoredPosition = startPos;
            }

            float duration = Mathf.Max(fadeDuration, slideDuration);
            if (animationType == AnimationType.Fade) duration = fadeDuration;

            while (time < duration)
            {
                time += Time.deltaTime;
                float t = Mathf.Clamp01(time / duration);

                if (animationType == AnimationType.Fade || animationType == AnimationType.FadeAndSlideUp)
                {
                    float fadeT = Mathf.Clamp01(time / fadeDuration);
                    canvasGroup.alpha = Mathf.Lerp(alphaStart, alphaEnd, Mathf.SmoothStep(0f, 1f, fadeT));
                }

                if (animationType != AnimationType.Fade && rectTransform != null)
                {
                    float slideT = Mathf.Clamp01(time / slideDuration);
                    rectTransform.anchoredPosition = Vector2.Lerp(startPos, endPos, Mathf.SmoothStep(0f, 1f, slideT));
                }

                yield return null;
            }

            canvasGroup.alpha = alphaEnd;
            if (rectTransform != null)
                rectTransform.anchoredPosition = endPos;

            IsAnimating = false;
            OnShowComplete?.Invoke();
        }

        private IEnumerator HideCoroutine(Action onComplete)
        {
            IsAnimating = true;
            float time = 0f;
            float alphaStart = 1f;
            float alphaEnd = 0f;
            Vector2 startPos = originalPosition;
            Vector2 endPos = GetSlideStartPosition();

            float duration = Mathf.Max(fadeDuration, slideDuration);
            if (animationType == AnimationType.Fade) duration = fadeDuration;

            while (time < duration)
            {
                time += Time.deltaTime;
                float t = Mathf.Clamp01(time / duration);

                if (animationType == AnimationType.Fade || animationType == AnimationType.FadeAndSlideUp)
                {
                    float fadeT = Mathf.Clamp01(time / fadeDuration);
                    canvasGroup.alpha = Mathf.Lerp(alphaStart, alphaEnd, Mathf.SmoothStep(0f, 1f, fadeT));
                }

                if (animationType != AnimationType.Fade && rectTransform != null)
                {
                    float slideT = Mathf.Clamp01(time / slideDuration);
                    rectTransform.anchoredPosition = Vector2.Lerp(startPos, endPos, Mathf.SmoothStep(0f, 1f, slideT));
                }

                yield return null;
            }

            canvasGroup.alpha = alphaEnd;
            if (rectTransform != null)
                rectTransform.anchoredPosition = endPos;

            gameObject.SetActive(false);
            IsAnimating = false;
            
            onComplete?.Invoke();
            OnHideComplete?.Invoke();
        }

        private Vector2 GetSlideStartPosition()
        {
            Vector2 pos = originalPosition;
            switch (animationType)
            {
                case AnimationType.SlideUp:
                case AnimationType.FadeAndSlideUp:
                    pos.y -= slideOffset;
                    break;
                case AnimationType.SlideDown:
                    pos.y += slideOffset;
                    break;
                case AnimationType.SlideLeft:
                    pos.x += slideOffset;
                    break;
                case AnimationType.SlideRight:
                    pos.x -= slideOffset;
                    break;
            }
            return pos;
        }
    }
}
