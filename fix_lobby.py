import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = '''        private void HandlePhaseChanged(GamePhase phase)
        {
            if (lobbyPanel == null) return;

            if (phase == GamePhase.Lobby)
            {
                if (AudioManager.Instance != null) AudioManager.Instance.PlayBGM("bgm_lobby");
                // Returning to the lobby (e.g. after the ending) must re-enable "New Game".
                isStartingGame = false;
                lobbyPanel.SetActive(true);
                UpdateContinueButton();
                StopAllCoroutines();
                StartCoroutine(SlideLobby(true));
            }
            else
            {
                StopAllCoroutines();
                StartCoroutine(SlideLobby(false));
            }
        }'''

new_code = '''        private void HandlePhaseChanged(GamePhase phase)
        {
            if (lobbyPanel == null) return;

            if (phase == GamePhase.Lobby)
            {
                if (AudioManager.Instance != null) AudioManager.Instance.PlayBGM("bgm_lobby");
                // Returning to the lobby (e.g. after the ending) must re-enable "New Game".
                isStartingGame = false;
                lobbyPanel.SetActive(true);
                UpdateContinueButton();
                StopAllCoroutines();
                if (gameObject.activeInHierarchy) StartCoroutine(SlideLobby(true));
            }
            else
            {
                StopAllCoroutines();
                if (gameObject.activeInHierarchy) StartCoroutine(SlideLobby(false));
            }
        }'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Fixed LobbyUI coroutine crash.")
else:
    print("Could not find the target code string.")
