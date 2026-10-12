import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_create = '''            splashCanvasGroup = splashRoot.AddComponent<CanvasGroup>();
            splashCanvasGroup.alpha = 0f; // Start transparent to fade in from black'''

new_create = '''            splashCanvasGroup = splashRoot.AddComponent<CanvasGroup>();
            splashCanvasGroup.alpha = 1f; // Start immediately with a white screen'''

old_play = '''            CanvasGroup logoCG = splashRoot.transform.Find("StudioLogo").GetComponent<CanvasGroup>();
            
            // 2. Fade the white background in from the dark screen (1 second)
            float bgFadeInTime = 1.0f;
            float elapsed = 0f;
            while (elapsed < bgFadeInTime)
            {
                elapsed += Time.unscaledDeltaTime;
                splashCanvasGroup.alpha = Mathf.Clamp01(elapsed / bgFadeInTime);
                yield return null;
            }
            splashCanvasGroup.alpha = 1f;'''

new_play = '''            CanvasGroup logoCG = splashRoot.transform.Find("StudioLogo").GetComponent<CanvasGroup>();
            
            // 2. Skip fading the white background; it's already 1f
            float elapsed = 0f;'''

if old_create in content and old_play in content:
    content = content.replace(old_create, new_create)
    content = content.replace(old_play, new_play)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Replaced splash sequence successfully.")
else:
    print("Could not find the target code string.")
