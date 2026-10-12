import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/Effects/ScreenEffects.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'public Coroutine ShakeCamera\(float duration = 0\.5f, float magnitude = 10f\)\s*\{\s*if \(!HalloweenVN\.Core\.SettingsData\.EnableFlashingEffects\) return null;\s*if \(_mainCam == null\) _mainCam = Camera\.main;\s*if \(_mainCam == null\) return null;\s*if \(_activeShakeCoroutine != null\)\s*\{\s*StopCoroutine\(_activeShakeCoroutine\);\s*if \(_hasOriginalCameraPos\) _mainCam\.transform\.localPosition = _originalCameraPos;\s*\}'

replacement = r'''public Coroutine ShakeCamera(float duration = 0.5f, float magnitude = 10f)
        {
            if (!HalloweenVN.Core.SettingsData.EnableFlashingEffects) return null;
            if (_mainCam == null) _mainCam = Camera.main;

            if (_activeShakeCoroutine != null)
            {
                StopCoroutine(_activeShakeCoroutine);
                GameObject uiCanvas = GameObject.Find("MainCanvas");
                Transform target = uiCanvas != null ? uiCanvas.transform : (_mainCam != null ? _mainCam.transform : null);
                if (_hasOriginalCameraPos && target != null) target.localPosition = _originalCameraPos;
            }'''

new_content = re.sub(pattern, replacement, content)
if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed ScreenEffects.cs ShakeCamera method!")
else:
    print("Failed to patch ShakeCamera method!")
