import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/Effects/ScreenEffects.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'private IEnumerator ShakeCameraCoroutine\(float duration, float magnitude\)\s*\{\s*if \(_mainCam == null\) yield break;\s*_originalCameraPos = _mainCam\.transform\.localPosition;\s*_hasOriginalCameraPos = true;\s*float elapsed = 0f;\s*while \(elapsed < duration\)\s*\{\s*if \(_mainCam == null\) break;\s*float offsetX = Random\.Range\(-1f, 1f\) \* magnitude;\s*float offsetY = Random\.Range\(-1f, 1f\) \* magnitude;\s*_mainCam\.transform\.localPosition = _originalCameraPos \+ new Vector3\(offsetX, offsetY, 0f\);\s*elapsed \+= Time\.unscaledDeltaTime \* \(IsFastForwarding \? 10f : 1f\);\s*yield return null;\s*\}\s*if \(_mainCam != null\) _mainCam\.transform\.localPosition = _originalCameraPos;\s*_hasOriginalCameraPos = false;\s*_activeShakeCoroutine = null;\s*\}'

replacement = r'''private IEnumerator ShakeCameraCoroutine(float duration, float magnitude)
        {
            GameObject uiCanvas = GameObject.Find("MainCanvas");
            Transform target = uiCanvas != null ? uiCanvas.transform : (_mainCam != null ? _mainCam.transform : null);
            if (target == null) yield break;

            _originalCameraPos = target.localPosition;
            _hasOriginalCameraPos = true;
            float elapsed = 0f;

            while (elapsed < duration)
            {
                if (target == null) break;
                float offsetX = Random.Range(-1f, 1f) * magnitude;
                float offsetY = Random.Range(-1f, 1f) * magnitude;
                target.localPosition = _originalCameraPos + new Vector3(offsetX, offsetY, 0f);
                elapsed += Time.unscaledDeltaTime * (IsFastForwarding ? 10f : 1f);
                yield return null;
            }

            if (target != null) target.localPosition = _originalCameraPos;
            _hasOriginalCameraPos = false;
            _activeShakeCoroutine = null;
        }'''

new_content = re.sub(pattern, replacement, content)
if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed ScreenEffects.cs ShakeCamera!")
else:
    print("Failed to patch ScreenEffects.cs!")
