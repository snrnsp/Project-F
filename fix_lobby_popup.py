import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target_start = '''        private void StartNewGame(GameObject popupOverlay)
        {
            Theme.ScreenTransition transition = FindFirstObjectByType<Theme.ScreenTransition>();
            if (transition != null)
            {
                // Run the coroutine on the transition object so it survives LobbyUI deactivation
                transition.StartCoroutine(DelayedNewGameRoutine(transition, popupOverlay));
            }
            else
            {
                if (popupOverlay != null) Destroy(popupOverlay);
                
                if (GameManager.Instance != null) GameManager.Instance.ChangePhase(GamePhase.Dialogue);
                if (DialogueManager.Instance != null) DialogueManager.Instance.StartDialogue("ch0_origin");
            }
        }'''

replacement_start = '''        private void StartNewGame(GameObject popupOverlay)
        {
            // Destroy the popup immediately so it doesn't linger during the fade out
            if (popupOverlay != null) Destroy(popupOverlay);

            Theme.ScreenTransition transition = FindFirstObjectByType<Theme.ScreenTransition>();
            if (transition != null)
            {
                // Run the coroutine on the transition object so it survives LobbyUI deactivation
                transition.StartCoroutine(DelayedNewGameRoutine(transition));
            }
            else
            {
                if (GameManager.Instance != null) GameManager.Instance.ChangePhase(GamePhase.Dialogue);
                if (DialogueManager.Instance != null) DialogueManager.Instance.StartDialogue("ch0_origin");
            }
        }'''

text = text.replace(target_start, replacement_start)

target_routine = '''        private IEnumerator DelayedNewGameRoutine(Theme.ScreenTransition transition, GameObject popupOverlay)
        {
            float fadeTime = 2.2f; // 0.3s faster than previous 2.5f
            float waitTime = 2.0f; // 2 seconds wait on black screen

            transition.autoTransitionOnPhaseChange = false;
            
            bool fadeOutDone = false;
            transition.FadeOut(fadeTime, () => fadeOutDone = true);
            
            // Wait for fade out to complete
            yield return new WaitUntil(() => fadeOutDone);
            
            // Screen is completely black here
            if (popupOverlay != null) Destroy(popupOverlay);'''

replacement_routine = '''        private IEnumerator DelayedNewGameRoutine(Theme.ScreenTransition transition)
        {
            float fadeTime = 2.2f; // 0.3s faster than previous 2.5f
            float waitTime = 2.0f; // 2 seconds wait on black screen

            transition.autoTransitionOnPhaseChange = false;
            
            bool fadeOutDone = false;
            transition.FadeOut(fadeTime, () => fadeOutDone = true);
            
            // Wait for fade out to complete
            yield return new WaitUntil(() => fadeOutDone);
            
            // Screen is completely black here'''

text = text.replace(target_routine, replacement_routine)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated StartNewGame to dismiss popup immediately')
