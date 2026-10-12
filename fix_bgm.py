import sys

# 1. Revert GameManager to Splash
filepath_gm = 'F:/Project-F/Assets/Scripts/Core/GameManager.cs'
with open(filepath_gm, 'r', encoding='utf-8') as f:
    gm_content = f.read()

gm_content = gm_content.replace('ChangePhase(GamePhase.Lobby);', 'ChangePhase(GamePhase.Splash);', 1) # Only replace the one in Start()

with open(filepath_gm, 'w', encoding='utf-8') as f:
    f.write(gm_content)

# 2. Update PlaySplashSequence in HalloweenUIBuilder
filepath_ui = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath_ui, 'r', encoding='utf-8-sig') as f:
    ui_content = f.read()

old_seq = '''            // 5. Briefly hold white screen
            yield return new UnityEngine.WaitForSecondsRealtime(0.5f);
            
            // Enable Lobby behind the white screen
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(true);
            
            // Fade the white background out to reveal Lobby'''

new_seq = '''            // 5. Briefly hold white screen
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
            
            // Fade the white background out to reveal Lobby'''

if old_seq in ui_content:
    ui_content = ui_content.replace(old_seq, new_seq)
    with open(filepath_ui, 'w', encoding='utf-8-sig') as f:
        f.write(ui_content)
    print("Fixed BGM issue by transitioning to Lobby after Splash.")
else:
    print("Could not find sequence to replace in UIBuilder.")
