import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add isStartingGame flag
if 'private bool isStartingGame = false;' not in text:
    target_vars = '        [SerializeField] private Text lobbyTitleText;'
    replacement_vars = '        [SerializeField] private Text lobbyTitleText;\n        private bool isStartingGame = false;'
    text = text.replace(target_vars, replacement_vars)

# 2. Fix the onClick listener
target_click = '''            btn.onClick.AddListener(() =>
            {
                btn.interactable = false; // Prevent double-clicks during fade
                StartNewGame(overlay);
            });'''

replacement_click = '''            btn.onClick.AddListener(() =>
            {
                if (isStartingGame) return;
                isStartingGame = true;
                if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
                
                // We do NOT set interactable = false here because it causes the button to permanently stay gray (disabled color)
                // during the long 2.2s fade out. The isStartingGame flag prevents double clicks instead.
                StartNewGame(overlay);
            });'''

text = text.replace(target_click, replacement_click)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed LobbyUI Confirm button state locking')
