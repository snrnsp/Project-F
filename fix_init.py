import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Make splashRoot active by default in CreateSplashUI
old_splash_end = '''            splashCanvasGroup.blocksRaycasts = true;
            
            splashRoot.SetActive(false);
        }'''
new_splash_end = '''            splashCanvasGroup.blocksRaycasts = true;
            
            splashRoot.SetActive(true); // Active immediately to cover the screen
        }'''

# Remove the explicit Lobby enable in Start()
old_start = '''        void Start()
        {
            // Start in Lobby ??hide all game panels
            if (dialoguePanelRoot) dialoguePanelRoot.SetActive(false);
            if (investigationPanelRoot) investigationPanelRoot.SetActive(false);
            if (deductionPanelRoot) deductionPanelRoot.SetActive(false);

            // Show lobby
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(true);'''

new_start = '''        void Start()
        {
            if (dialoguePanelRoot) dialoguePanelRoot.SetActive(false);
            if (investigationPanelRoot) investigationPanelRoot.SetActive(false);
            if (deductionPanelRoot) deductionPanelRoot.SetActive(false);
            if (lobbyPanelRoot) lobbyPanelRoot.SetActive(false);'''

content = content.replace(old_splash_end, new_splash_end)
content = content.replace(old_start, new_start)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated HalloweenUIBuilder initialization.")
