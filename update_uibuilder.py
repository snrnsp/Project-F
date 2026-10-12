import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update OnPhaseChanged
old_phase = '''        private void OnPhaseChanged(GamePhase phase)
        {
            if (splashRoot != null && splashRoot.activeSelf && phase == GamePhase.Lobby)
            {
                if (lobbyPanelRoot) lobbyPanelRoot.SetActive(false);
            }
            else
            {
                if (lobbyPanelRoot) lobbyPanelRoot.SetActive(phase == GamePhase.Lobby);
            }'''

new_phase = '''        private void OnPhaseChanged(GamePhase phase)
        {
            if (splashRoot != null)
            {
                if (phase == GamePhase.Splash)
                {
                    StartCoroutine(PlaySplashSequence());
                }
            }
            
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(phase == GamePhase.Lobby);'''

content = content.replace(old_phase, new_phase)

# 2. In PlaySplashSequence, remove the explicit lobby toggle, and call ChangePhase(Lobby) at the end.
old_seq = '''        private System.Collections.IEnumerator PlaySplashSequence()
        {
            // Instantly hide lobby and show splash
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
            }
            logoCG.alpha = 1f;
            
            // 3. Hold
            yield return new UnityEngine.WaitForSecondsRealtime(2.0f);
            
            // 4. Fade Logo Out
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                logoCG.alpha = 1f - (t / fadeTime);
                yield return null;
            }
            logoCG.alpha = 0f;
            
            // 5. Briefly hold white screen, then reveal Lobby
            yield return new UnityEngine.WaitForSecondsRealtime(0.5f);
            
            // Enable Lobby behind the white screen
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(true);
            
            // Fade the white background out to reveal Lobby
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                splashCanvasGroup.alpha = 1f - (t / fadeTime);
                yield return null;
            }
            splashCanvasGroup.alpha = 0f;
            
            splashRoot.SetActive(false);
            splashCanvasGroup.blocksRaycasts = false;
        }'''

new_seq = '''        private System.Collections.IEnumerator PlaySplashSequence()
        {
            splashRoot.SetActive(true);
            splashRoot.transform.SetAsLastSibling(); 
            
            CanvasGroup logoCG = splashRoot.transform.Find("StudioLogo").GetComponent<CanvasGroup>();
            
            float fadeTime = 1.0f;
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                logoCG.alpha = t / fadeTime;
                yield return null;
            }
            logoCG.alpha = 1f;
            
            yield return new UnityEngine.WaitForSecondsRealtime(2.0f);
            
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                logoCG.alpha = 1f - (t / fadeTime);
                yield return null;
            }
            logoCG.alpha = 0f;
            
            yield return new UnityEngine.WaitForSecondsRealtime(0.5f);
            
            // Trigger phase change to Lobby! This will fire OnPhaseChanged across all scripts.
            if (HalloweenVN.Core.GameManager.Instance != null)
            {
                HalloweenVN.Core.GameManager.Instance.ChangePhase(HalloweenVN.Core.GamePhase.Lobby);
            }
            else
            {
                if (lobbyPanelRoot) lobbyPanelRoot.SetActive(true);
            }
            
            // Now fade the white background out to reveal Lobby
            for (float t = 0; t < fadeTime; t += Time.unscaledDeltaTime)
            {
                splashCanvasGroup.alpha = 1f - (t / fadeTime);
                yield return null;
            }
            splashCanvasGroup.alpha = 0f;
            
            splashRoot.SetActive(false);
            splashCanvasGroup.blocksRaycasts = false;
        }'''

content = content.replace(old_seq, new_seq)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HalloweenUIBuilder")
