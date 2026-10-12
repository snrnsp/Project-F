import codecs

filepath = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 1. Modify Start()
old_start = '''        private void Start()
        {
            if (newGameButton != null)
            {'''
new_start = '''        private void Start()
        {
            ShowPreAlphaWarning(); // Added to show on boot

            if (newGameButton != null)
            {'''
content = content.replace(old_start, new_start)

# 2. Modify OnNewGameClicked()
old_new_game = '''        private void OnNewGameClicked()
        {
            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
            ShowPreAlphaWarning();
        }'''
new_new_game = '''        private void OnNewGameClicked()
        {
            if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
            if (isStartingGame) return;
            isStartingGame = true;
            StartNewGame(null);
        }'''
content = content.replace(old_new_game, new_new_game)

# 3. Modify Photosensitivity OK button
old_photo_ok = '''            btn.onClick.AddListener(() =>
            {
                if (isStartingGame) return;
                isStartingGame = true;
                if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
                
                // We do NOT set interactable = false here because it causes the button to permanently stay gray (disabled color)
                // during the long 2.2s fade out. The isStartingGame flag prevents double clicks instead.
                StartNewGame(overlay);
            });'''
new_photo_ok = '''            btn.onClick.AddListener(() =>
            {
                if (UnityEngine.EventSystems.EventSystem.current != null) UnityEngine.EventSystems.EventSystem.current.SetSelectedGameObject(null);
                Destroy(overlay);
            });'''
content = content.replace(old_photo_ok, new_photo_ok)

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("Updated LobbyUI.cs for boot notices!")
