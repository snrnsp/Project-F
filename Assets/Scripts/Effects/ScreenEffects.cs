using UnityEngine;
using UnityEngine.UI;
using System.Collections;

namespace HalloweenVN.Effects
{
    /// <summary>
    /// Screen effects manager ported from old project.
    /// Handles camera shake, screen flash, fade to/from black, and screen tint.
    /// </summary>
    public class ScreenEffects : MonoBehaviour
    {
        public static ScreenEffects Instance { get; private set; }

        private Image flashOverlay;
        private Image fadeOverlay;
        private Coroutine _activeShakeCoroutine;
        private Coroutine _activeFlashCoroutine;
        private Coroutine _activeFadeCoroutine;
        private Vector3 _originalCameraPos;
        private bool _hasOriginalCameraPos;
        private Camera _mainCam;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;

            // Flash Canvas (highest sorting order)
            flashOverlay = CreateOverlayImage("FlashCanvas", 999);
            flashOverlay.gameObject.SetActive(false);

            // Fade Canvas
            fadeOverlay = CreateOverlayImage("FadeCanvas", 998);
            fadeOverlay.gameObject.SetActive(false);
        }

        private Image CreateOverlayImage(string canvasName, int sortingOrder)
        {
            GameObject canvasObj = new GameObject(canvasName);
            canvasObj.transform.SetParent(transform);
            Canvas canvas = canvasObj.AddComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;
            canvas.sortingOrder = sortingOrder;

            GameObject imgObj = new GameObject("Overlay");
            imgObj.transform.SetParent(canvasObj.transform, false);
            RectTransform rt = imgObj.AddComponent<RectTransform>();
            rt.anchorMin = Vector2.zero;
            rt.anchorMax = Vector2.one;
            rt.offsetMin = Vector2.zero;
            rt.offsetMax = Vector2.zero;

            Image img = imgObj.AddComponent<Image>();
            img.color = Color.clear;
            img.raycastTarget = false;
            return img;
        }

        // ═══════════ Camera Shake ═══════════
        public Coroutine ShakeCamera(float duration = 0.5f, float magnitude = 10f)
        {
            if (_mainCam == null) _mainCam = Camera.main;
            if (_mainCam == null) return null;

            if (_activeShakeCoroutine != null)
            {
                StopCoroutine(_activeShakeCoroutine);
                if (_hasOriginalCameraPos) _mainCam.transform.localPosition = _originalCameraPos;
            }
            _activeShakeCoroutine = StartCoroutine(ShakeCameraCoroutine(duration, magnitude));
            return _activeShakeCoroutine;
        }

        private IEnumerator ShakeCameraCoroutine(float duration, float magnitude)
        {
            if (_mainCam == null) yield break;

            _originalCameraPos = _mainCam.transform.localPosition;
            _hasOriginalCameraPos = true;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                if (_mainCam == null) break;
                float offsetX = Random.Range(-1f, 1f) * magnitude;
                float offsetY = Random.Range(-1f, 1f) * magnitude;
                _mainCam.transform.localPosition = _originalCameraPos + new Vector3(offsetX, offsetY, 0f);
                elapsed += Time.unscaledDeltaTime;
                yield return null;
            }

            if (_mainCam != null) _mainCam.transform.localPosition = _originalCameraPos;
            _hasOriginalCameraPos = false;
            _activeShakeCoroutine = null;
        }

        // ═══════════ Screen Flash ═══════════
        public Coroutine FlashScreen(Color color, float duration = 0.5f)
        {
            if (_activeFlashCoroutine != null) StopCoroutine(_activeFlashCoroutine);
            _activeFlashCoroutine = StartCoroutine(FlashScreenCoroutine(color, duration));
            return _activeFlashCoroutine;
        }

        private IEnumerator FlashScreenCoroutine(Color color, float duration)
        {
            if (flashOverlay == null) yield break;

            flashOverlay.gameObject.SetActive(true);
            flashOverlay.color = color;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                elapsed += Time.unscaledDeltaTime;
                float alpha = Mathf.Lerp(color.a, 0f, elapsed / duration);
                flashOverlay.color = new Color(color.r, color.g, color.b, alpha);
                yield return null;
            }

            flashOverlay.color = Color.clear;
            flashOverlay.gameObject.SetActive(false);
            _activeFlashCoroutine = null;
        }

        // ═══════════ Fade To/From Black ═══════════
        public Coroutine FadeToBlack(float duration = 1f)
        {
            if (_activeFadeCoroutine != null) StopCoroutine(_activeFadeCoroutine);
            _activeFadeCoroutine = StartCoroutine(FadeCoroutine(Color.clear, Color.black, duration));
            return _activeFadeCoroutine;
        }

        public Coroutine FadeFromBlack(float duration = 1f)
        {
            if (_activeFadeCoroutine != null) StopCoroutine(_activeFadeCoroutine);
            _activeFadeCoroutine = StartCoroutine(FadeCoroutine(new Color(0, 0, 0, 1), Color.clear, duration));
            return _activeFadeCoroutine;
        }

        private IEnumerator FadeCoroutine(Color from, Color to, float duration)
        {
            if (fadeOverlay == null) yield break;

            fadeOverlay.gameObject.SetActive(true);
            float elapsed = 0f;

            while (elapsed < duration)
            {
                elapsed += Time.unscaledDeltaTime;
                float t = Mathf.SmoothStep(0f, 1f, elapsed / duration);
                fadeOverlay.color = Color.Lerp(from, to, t);
                yield return null;
            }

            fadeOverlay.color = to;
            if (to.a <= 0.01f)
            {
                fadeOverlay.gameObject.SetActive(false);
            }
            _activeFadeCoroutine = null;
        }
    }
}
