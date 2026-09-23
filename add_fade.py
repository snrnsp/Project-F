import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Add state tracker and coroutine variable
state_tracker = '''        private bool isUiHidden = false;
        private bool _currentlyInDialoguePanel = true;
        private Coroutine panelTransitionCoroutine;'''
text = text.replace('private bool isUiHidden = false;', state_tracker)

# Replace the panel switching logic in ProcessNode
target_switch = '''            if (usePanel)
            {
                // Show dialogue panel, hide narrator
                if (dialoguePanel != null) dialoguePanel.SetActive(true);
                if (narratorText != null && narratorText.transform.parent != null)
                {
                    narratorText.transform.parent.gameObject.SetActive(false);
                }
                if (dialogueText != null) dialogueText.alignment = TextAlignmentOptions.TopLeft;
            }
            else
            {
                EnsureNarratorText();
                // Hide dialogue panel, show fullscreen narrator
                if (dialoguePanel != null) dialoguePanel.SetActive(false);
                if (narratorText != null && narratorText.transform.parent != null)
                {
                    narratorText.transform.parent.gameObject.SetActive(true);
                }
                fullText = "<b>" + fullText + "</b>";
            }'''

replacement_switch = '''            if (!usePanel)
            {
                EnsureNarratorText();
                fullText = "<b>" + fullText + "</b>";
            }
            else
            {
                if (dialogueText != null) dialogueText.alignment = TextAlignmentOptions.TopLeft;
            }

            if (usePanel != _currentlyInDialoguePanel)
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
text = text.replace(target_switch, replacement_switch)

# Add CrossfadePanels Coroutine
crossfade_code = '''
        private System.Collections.IEnumerator CrossfadePanels(bool toDialogue)
        {
            GameObject narratorParent = narratorText != null ? narratorText.transform.parent.gameObject : null;
            if (dialoguePanel == null || narratorParent == null) yield break;

            CanvasGroup diagCG = dialoguePanel.GetComponent<CanvasGroup>();
            if (diagCG == null) diagCG = dialoguePanel.AddComponent<CanvasGroup>();

            CanvasGroup narrCG = narratorParent.GetComponent<CanvasGroup>();
            if (narrCG == null) narrCG = narratorParent.AddComponent<CanvasGroup>();

            float duration = 0.4f;
            float elapsed = 0f;

            float startDiagAlpha = diagCG.alpha;
            float startNarrAlpha = narrCG.alpha;

            if (toDialogue)
            {
                dialoguePanel.SetActive(true);
                while (elapsed < duration)
                {
                    elapsed += Time.deltaTime;
                    float t = elapsed / duration;
                    diagCG.alpha = Mathf.SmoothStep(startDiagAlpha, 1f, t);
                    narrCG.alpha = Mathf.SmoothStep(startNarrAlpha, 0f, t);
                    yield return null;
                }
                diagCG.alpha = 1f;
                narrCG.alpha = 0f;
                narratorParent.SetActive(false);
            }
            else
            {
                narratorParent.SetActive(true);
                while (elapsed < duration)
                {
                    elapsed += Time.deltaTime;
                    float t = elapsed / duration;
                    narrCG.alpha = Mathf.SmoothStep(startNarrAlpha, 1f, t);
                    diagCG.alpha = Mathf.SmoothStep(startDiagAlpha, 0f, t);
                    yield return null;
                }
                narrCG.alpha = 1f;
                diagCG.alpha = 0f;
                dialoguePanel.SetActive(false);
            }
        }
'''
text = text.replace('// =========== Background ===========', crossfade_code + '\n        // =========== Background ===========')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added crossfade for narrator monologues')
