import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''            // Hold the empty white screen a bit longer before transitioning
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
            float bgFadeTime = 2.0f;'''

new_code = '''            // Hold the empty white screen briefly before transitioning
            yield return new UnityEngine.WaitForSecondsRealtime(1.0f);
            
            // Prevent the default black screen transition from firing
            var transition = UnityEngine.Object.FindFirstObjectByType<HalloweenVN.UI.Theme.ScreenTransition>();
            if (transition != null) transition.autoTransitionOnPhaseChange = false;

            // Trigger phase change to Lobby! This will fire OnPhaseChanged across all scripts.
            if (HalloweenVN.Core.GameManager.Instance != null)
            {
                HalloweenVN.Core.GameManager.Instance.ChangePhase(HalloweenVN.Core.GamePhase.Lobby);
            }
            else
            {
                if (lobbyPanelRoot) lobbyPanelRoot.SetActive(true);
            }
            
            // Re-enable auto transition for future phase changes
            if (transition != null) transition.autoTransitionOnPhaseChange = true;
            
            // Now fade the white background out to reveal Lobby
            float bgFadeTime = 1.0f;'''

content = content.replace(old_code, new_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated splash screen transition logic and speed.")
