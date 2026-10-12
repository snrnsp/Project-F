import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 1. Update CreateSplashUI to not hide it and set alpha to 0
old_create = '''            splashCanvasGroup = splashRoot.AddComponent<CanvasGroup>();
            splashCanvasGroup.alpha = 1f; // Background starts fully opaque
            splashCanvasGroup.blocksRaycasts = true;
            
            splashRoot.SetActive(false);
        }'''
new_create = '''            splashCanvasGroup = splashRoot.AddComponent<CanvasGroup>();
            splashCanvasGroup.alpha = 0f; // Start transparent to fade in from black
            splashCanvasGroup.blocksRaycasts = true;
            
            splashRoot.SetActive(true); // Keep it active from frame 1
        }'''

# 2. Update PlaySplashSequence to fade in the background first
old_seq = '''        private System.Collections.IEnumerator PlaySplashSequence()
        {
            yield return null; 

            // 1. Hide Lobby while Splash is playing
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(false);

            splashRoot.SetActive(true);
            splashRoot.transform.SetAsLastSibling(); 
            
            CanvasGroup logoCG = splashRoot.transform.Find("StudioLogo").GetComponent<CanvasGroup>();
            
            // 2. Fade Logo In (Background is already white)
            float fadeTime = 1.0f;
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                logoCG.alpha = t / fadeTime;
                yield return null;
            }'''
new_seq = '''        private System.Collections.IEnumerator PlaySplashSequence()
        {
            // 1. Hide Lobby while Splash is playing
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(false);

            splashRoot.transform.SetAsLastSibling(); 
            
            CanvasGroup logoCG = splashRoot.transform.Find("StudioLogo").GetComponent<CanvasGroup>();
            
            // 2. Fade the white background in from the dark screen
            float bgFadeInTime = 1.0f;
            for (float t = 0; t < bgFadeInTime; t += Time.unscaledDeltaTime)
            {
                splashCanvasGroup.alpha = t / bgFadeInTime;
                yield return null;
            }
            splashCanvasGroup.alpha = 1f;

            // 3. Fade Logo In (Background is now white)
            float fadeTime = 1.0f;
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                logoCG.alpha = t / fadeTime;
                yield return null;
            }'''

if old_create in content and old_seq in content:
    content = content.replace(old_create, new_create)
    content = content.replace(old_seq, new_seq)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Updated Splash to fade in from dark.")
else:
    print("Could not find blocks to replace.")
