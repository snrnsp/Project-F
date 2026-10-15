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
        private bool _isContinuousShake;
        private Coroutine _activeFlashCoroutine;
        private Coroutine _activeFadeCoroutine;
        private Vector3 _originalCameraPos;
        private Vector3 _originalDialoguePanelPos;
        private Vector3 _originalHudRootPos;
        private bool _hasOriginalCameraPos;
        private Camera _mainCam;
        private Transform _uiCanvasTransform;
        private Transform _dialoguePanelTransform;
        private Transform _hudRootTransform;

        private Transform GetShakeTarget()
        {
            if (_uiCanvasTransform == null)
            {
                // Target DialogueRoot (child RectTransform) instead of MainCanvas (root ScreenSpaceOverlay Canvas,
                // whose localPosition is locked by Unity's Canvas layout system).
                GameObject dlgRoot = GameObject.Find("DialogueRoot");
                if (dlgRoot != null) _uiCanvasTransform = dlgRoot.transform;
                else
                {
                    GameObject uiCanvas = GameObject.Find("MainCanvas");
                    if (uiCanvas != null) _uiCanvasTransform = uiCanvas.transform;
                }
            }
            if (_uiCanvasTransform != null)
            {
                if (_dialoguePanelTransform == null) _dialoguePanelTransform = _uiCanvasTransform.Find("DialoguePanel");
                if (_hudRootTransform == null) _hudRootTransform = _uiCanvasTransform.Find("DialogueHudRoot");
                return _uiCanvasTransform;
            }
            if (_mainCam == null) _mainCam = Camera.main;
            return _mainCam != null ? _mainCam.transform : null;
        }

        private void CaptureOriginalPositions(Transform target)
        {
            if (target == null || _hasOriginalCameraPos) return;
            _originalCameraPos = target.localPosition;
            if (_dialoguePanelTransform != null) _originalDialoguePanelPos = _dialoguePanelTransform.localPosition;
            if (_hudRootTransform != null) _originalHudRootPos = _hudRootTransform.localPosition;
            _hasOriginalCameraPos = true;
        }

        private void ResetOriginalPositions(Transform target)
        {
            if (!_hasOriginalCameraPos) return;
            if (target != null) target.localPosition = _originalCameraPos;
            if (_dialoguePanelTransform != null) _dialoguePanelTransform.localPosition = _originalDialoguePanelPos;
            if (_hudRootTransform != null) _hudRootTransform.localPosition = _originalHudRootPos;
            _hasOriginalCameraPos = false;
        }
        
        private bool IsFastForwarding => HalloweenVN.Core.SettingsData.IsSkipKeyPressed();

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
            if (!HalloweenVN.Core.SettingsData.EnableFlashingEffects) return null;
            if (_isContinuousShake) return _activeShakeCoroutine;

            Transform target = GetShakeTarget();
            if (_activeShakeCoroutine != null)
            {
                StopCoroutine(_activeShakeCoroutine);
                ResetOriginalPositions(target);
            }
            _activeShakeCoroutine = StartCoroutine(ShakeCameraCoroutine(duration, magnitude));
            return _activeShakeCoroutine;
        }

        private IEnumerator ShakeCameraCoroutine(float duration, float magnitude)
        {
            Transform target = GetShakeTarget();
            if (target == null) yield break;

            CaptureOriginalPositions(target);
            float elapsed = 0f;

            while (elapsed < duration)
            {
                if (target == null) break;
                if (!HalloweenVN.Core.SettingsData.EnableFlashingEffects)
                {
                    target.localPosition = _originalCameraPos;
                    break;
                }
                float offsetX = Random.Range(-1f, 1f) * magnitude;
                float offsetY = Random.Range(-1f, 1f) * magnitude;
                target.localPosition = _originalCameraPos + new Vector3(offsetX, offsetY, 0f);
                elapsed += Time.unscaledDeltaTime * (IsFastForwarding ? 10f : 1f);
                yield return null;
            }

            if (!_isContinuousShake)
            {
                ResetOriginalPositions(target);
                _activeShakeCoroutine = null;
            }
        }

        private float _continuousMagnitude = 10f;

        public Coroutine StartContinuousShake(float magnitude = 10f)
        {
            if (_activeShakeCoroutine != null)
            {
                StopCoroutine(_activeShakeCoroutine);
                Transform prevTarget = GetShakeTarget();
                ResetOriginalPositions(prevTarget);
            }
            _isContinuousShake = true;
            _continuousMagnitude = magnitude;
            _activeShakeCoroutine = StartCoroutine(ContinuousShakeCoroutine(magnitude));
            return _activeShakeCoroutine;
        }

        private IEnumerator ContinuousShakeCoroutine(float magnitude)
        {
            Transform target = GetShakeTarget();
            CaptureOriginalPositions(target);

            while (_isContinuousShake)
            {
                if (target == null)
                {
                    target = GetShakeTarget();
                    CaptureOriginalPositions(target);
                }
                if (target != null)
                {
                    if (HalloweenVN.Core.SettingsData.EnableFlashingEffects)
                    {
                        float offsetX = Random.Range(-1f, 1f) * magnitude;
                        float offsetY = Random.Range(-1f, 1f) * magnitude;
                        Vector3 offset = new Vector3(offsetX, offsetY, 0f);
                        target.localPosition = _originalCameraPos + offset;
                        if (_dialoguePanelTransform != null) _dialoguePanelTransform.localPosition = _originalDialoguePanelPos - offset;
                        if (_hudRootTransform != null) _hudRootTransform.localPosition = _originalHudRootPos - offset;
                    }
                    else
                    {
                        target.localPosition = _originalCameraPos;
                        if (_dialoguePanelTransform != null) _dialoguePanelTransform.localPosition = _originalDialoguePanelPos;
                        if (_hudRootTransform != null) _hudRootTransform.localPosition = _originalHudRootPos;
                    }
                }
                yield return null;
            }

            ResetOriginalPositions(target);
            _activeShakeCoroutine = null;
        }

        public void StopShake(float fadeDuration = 0f)
        {
            bool wasContinuous = _isContinuousShake;
            _isContinuousShake = false;
            if (_activeShakeCoroutine != null)
            {
                StopCoroutine(_activeShakeCoroutine);
                _activeShakeCoroutine = null;
            }

            if (fadeDuration > 0f && wasContinuous && HalloweenVN.Core.SettingsData.EnableFlashingEffects && gameObject.activeInHierarchy)
            {
                _activeShakeCoroutine = StartCoroutine(FadeOutShakeCoroutine(_continuousMagnitude, fadeDuration));
                return;
            }

            Transform target = GetShakeTarget();
            ResetOriginalPositions(target);
        }

        private IEnumerator FadeOutShakeCoroutine(float startMagnitude, float duration)
        {
            Transform target = GetShakeTarget();
            if (target == null)
            {
                _hasOriginalCameraPos = false;
                _activeShakeCoroutine = null;
                yield break;
            }

            CaptureOriginalPositions(target);

            float elapsed = 0f;
            while (elapsed < duration)
            {
                if (target == null) break;
                if (!HalloweenVN.Core.SettingsData.EnableFlashingEffects)
                {
                    break;
                }
                elapsed += Time.unscaledDeltaTime * (IsFastForwarding ? 10f : 1f);
                float t = Mathf.Clamp01(elapsed / duration);
                float currentMag = Mathf.Lerp(startMagnitude, 0f, Mathf.SmoothStep(0f, 1f, t));
                float offsetX = Random.Range(-1f, 1f) * currentMag;
                float offsetY = Random.Range(-1f, 1f) * currentMag;
                Vector3 offset = new Vector3(offsetX, offsetY, 0f);
                target.localPosition = _originalCameraPos + offset;
                if (_dialoguePanelTransform != null) _dialoguePanelTransform.localPosition = _originalDialoguePanelPos - offset;
                if (_hudRootTransform != null) _hudRootTransform.localPosition = _originalHudRootPos - offset;
                yield return null;
            }

            ResetOriginalPositions(target);
            _activeShakeCoroutine = null;
        }

        // ═══════════ Screen Flash ═══════════
        public Coroutine FlashScreen(Color color, float duration = 0.5f)
        {
            if (!HalloweenVN.Core.SettingsData.EnableFlashingEffects) return null;
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
                if (!HalloweenVN.Core.SettingsData.EnableFlashingEffects) break;
                elapsed += Time.unscaledDeltaTime * (IsFastForwarding ? 10f : 1f);
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
                elapsed += Time.unscaledDeltaTime * (IsFastForwarding ? 10f : 1f);
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
