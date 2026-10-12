import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_splash = '''            splashCanvasGroup = splashRoot.AddComponent<CanvasGroup>();
            splashCanvasGroup.alpha = 0f; // Start transparent to fade in from black
            splashCanvasGroup.blocksRaycasts = true;
            
            // 1. Hide Lobby while Splash is playing
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(false);

            splashRoot.transform.SetAsLastSibling(); 
            
            CanvasGroup logoCG = splashRoot.transform.Find("StudioLogo").GetComponent<CanvasGroup>();
            
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

new_splash = '''            splashCanvasGroup = splashRoot.AddComponent<CanvasGroup>();
            splashCanvasGroup.alpha = 1f; // Start immediately as white screen
            splashCanvasGroup.blocksRaycasts = true;
            
            // 1. Hide Lobby while Splash is playing
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(false);

            splashRoot.transform.SetAsLastSibling(); 
            
            CanvasGroup logoCG = splashRoot.transform.Find("StudioLogo").GetComponent<CanvasGroup>();
            
            // 2. Skip fading the white background; it's already 1f
            float elapsed = 0f;'''

if old_splash in content:
    content = content.replace(old_splash, new_splash)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Replaced splash sequence successfully.")
else:
    print("Could not find the target code string.")
