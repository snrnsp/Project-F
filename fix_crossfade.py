import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the transition call in UpdateUI
target_update = '''            if (usePanel != _currentlyInDialoguePanel)
            {
                _currentlyInDialoguePanel = usePanel;
                if (panelTransitionCoroutine != null) StopCoroutine(panelTransitionCoroutine);
                if (gameObject.activeInHierarchy)
                {
                    panelTransitionCoroutine = StartCoroutine(CrossfadePanels(usePanel));
                }
                else
                {
                    // Instant if inactive
                    if (dialoguePanel != null) dialoguePanel.SetActive(usePanel);
                    if (narratorText != null && narratorText.transform.parent != null)
                    {
                        narratorText.transform.parent.gameObject.SetActive(!usePanel);
                    }
                }
            }
            else
            {
                // Ensure visibility if no transition needed
                if (dialoguePanel != null) dialoguePanel.SetActive(usePanel);
                if (narratorText != null && narratorText.transform.parent != null)
                {
                    narratorText.transform.parent.gameObject.SetActive(!usePanel);
                }
            }'''

replacement_update = '''            _currentlyInDialoguePanel = usePanel;
            if (dialoguePanel != null) dialoguePanel.SetActive(usePanel);
            if (narratorText != null && narratorText.transform.parent != null)
            {
                narratorText.transform.parent.gameObject.SetActive(!usePanel);
            }'''

text = text.replace(target_update, replacement_update)

# 2. Remove panelTransitionCoroutine variable
text = text.replace('private Coroutine panelTransitionCoroutine;', '')

# 3. Remove CrossfadePanels method
target_crossfade = '''        private System.Collections.IEnumerator CrossfadePanels(bool toDialogue)
        {
            GameObject narratorParent = narratorText != null ? narratorText.transform.parent.gameObject : null;
            if (dialoguePanel == null || narratorParent == null) yield break;

            CanvasGroup dialogueCg = dialoguePanel.GetComponent<CanvasGroup>();
            if (dialogueCg == null) dialogueCg = dialoguePanel.AddComponent<CanvasGroup>();

            CanvasGroup narratorCg = narratorParent.GetComponent<CanvasGroup>();
            if (narratorCg == null) narratorCg = narratorParent.AddComponent<CanvasGroup>();

            dialoguePanel.SetActive(true);
            narratorParent.SetActive(true);

            float duration = 0.4f;
            float elapsed = 0f;

            float startDialogueAlpha = dialogueCg.alpha;
            float targetDialogueAlpha = toDialogue ? 1f : 0f;

            float startNarratorAlpha = narratorCg.alpha;
            float targetNarratorAlpha = toDialogue ? 0f : 1f;

            while (elapsed < duration)
            {
                elapsed += Time.deltaTime;
                float t = elapsed / duration;

                dialogueCg.alpha = Mathf.Lerp(startDialogueAlpha, targetDialogueAlpha, t);
                narratorCg.alpha = Mathf.Lerp(startNarratorAlpha, targetNarratorAlpha, t);

                yield return null;
            }

            dialogueCg.alpha = targetDialogueAlpha;
            narratorCg.alpha = targetNarratorAlpha;

            dialoguePanel.SetActive(toDialogue);
            narratorParent.SetActive(!toDialogue);
        }'''

text = text.replace(target_crossfade, '')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Removed CrossfadePanels and reverted to instant panel switching')
