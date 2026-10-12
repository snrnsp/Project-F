import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

start_marker = 'private System.Collections.IEnumerator PlaySplashSequence()'
end_marker = 'private void CreateLobbyUI()'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find bounds.")
    sys.exit(1)

new_coroutine = '''private System.Collections.IEnumerator PlaySplashSequence()
        {
            // Wait a few frames to let Unity stabilize its delta time after heavy initialization
            yield return null;
            yield return null;
            yield return null;

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
            splashCanvasGroup.alpha = 1f;

            // 3. Fade Logo In (1 second)
            elapsed = 0f;
            float fadeTime = 1.0f;
            while (elapsed < fadeTime)
            {
                elapsed += Time.unscaledDeltaTime;
                logoCG.alpha = Mathf.Clamp01(elapsed / fadeTime);
                yield return null;
            }
            logoCG.alpha = 1f;
            
            // 4. Hold Logo (2 seconds)
            yield return new UnityEngine.WaitForSecondsRealtime(2.0f);
            
            // 5. Fade Logo Out (1 second)
            elapsed = 0f;
            while (elapsed < fadeTime)
            {
                elapsed += Time.unscaledDeltaTime;
                logoCG.alpha = 1f - Mathf.Clamp01(elapsed / fadeTime);
                yield return null;
            }
            logoCG.alpha = 0f;
            
            // 6. Briefly hold empty white screen (0.5 seconds)
            yield return new UnityEngine.WaitForSecondsRealtime(0.5f);
            
            // Prevent the default black screen transition from firing when phase changes
            var transition = UnityEngine.Object.FindFirstObjectByType<HalloweenVN.UI.Theme.ScreenTransition>();
            if (transition != null) transition.autoTransitionOnPhaseChange = false;

            // Trigger phase change to Lobby! This will fire OnPhaseChanged across all scripts and play BGM.
            if (HalloweenVN.Core.GameManager.Instance != null)
            {
                HalloweenVN.Core.GameManager.Instance.ChangePhase(HalloweenVN.Core.GamePhase.Lobby);
            }
            else
            {
                if (lobbyPanelRoot) lobbyPanelRoot.SetActive(true);
            }
            
            if (transition != null) transition.autoTransitionOnPhaseChange = true;
            
            // 7. Fade the white background out to reveal Lobby (1 second)
            elapsed = 0f;
            while (elapsed < bgFadeInTime)
            {
                elapsed += Time.unscaledDeltaTime;
                splashCanvasGroup.alpha = 1f - Mathf.Clamp01(elapsed / bgFadeInTime);
                yield return null;
            }
            splashCanvasGroup.alpha = 0f;
            
            splashRoot.SetActive(false);
            splashCanvasGroup.blocksRaycasts = false;
        }

        '''

content = content[:start_idx] + new_coroutine + content[end_idx:]

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Updated PlaySplashSequence for robustness.")
