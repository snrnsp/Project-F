import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Make OnPhaseChanged respect Splash Screen
old_phase = '''        private void OnPhaseChanged(GamePhase phase)
        {
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(phase == GamePhase.Lobby);'''

new_phase = '''        private void OnPhaseChanged(GamePhase phase)
        {
            if (splashRoot != null && splashRoot.activeSelf && phase == GamePhase.Lobby)
            {
                if (lobbyPanelRoot) lobbyPanelRoot.SetActive(false);
            }
            else
            {
                if (lobbyPanelRoot) lobbyPanelRoot.SetActive(phase == GamePhase.Lobby);
            }'''

# Fix 2: Remove yield return null at the start of PlaySplashSequence so it happens instantly
old_coroutine = '''        private System.Collections.IEnumerator PlaySplashSequence()
        {
            yield return null; 

            // 1. Hide Lobby while Splash is playing
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(false);'''

new_coroutine = '''        private System.Collections.IEnumerator PlaySplashSequence()
        {
            // Instantly hide lobby and show splash
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(false);'''

content = content.replace(old_phase, new_phase)
content = content.replace(old_coroutine, new_coroutine)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HalloweenUIBuilder.")
