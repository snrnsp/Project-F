import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''            yield return new UnityEngine.WaitForSecondsRealtime(0.5f);
            
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
            }'''

new_code = '''            // Hold the empty white screen a bit longer before transitioning
            yield return new UnityEngine.WaitForSecondsRealtime(1.5f);
            
            // Trigger phase change to Lobby! This will fire OnPhaseChanged across all scripts.
            if (HalloweenVN.Core.GameManager.Instance != null)
            {
                HalloweenVN.Core.GameManager.Instance.ChangePhase(HalloweenVN.Core.GamePhase.Lobby);
            }
            else
            {
                if (lobbyPanelRoot) lobbyPanelRoot.SetActive(true);
            }
            
            // Now fade the white background out SLOWLY to reveal Lobby
            float bgFadeTime = 2.0f;
            for (float t = 0; t < bgFadeTime; t += Time.unscaledDeltaTime)
            {
                splashCanvasGroup.alpha = 1f - (t / bgFadeTime);
                yield return null;
            }'''

content = content.replace(old_code, new_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated splash screen timing.")
