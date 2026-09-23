import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

update_code = '''
        private bool isUiHidden = false;

        private void Update()
        {
            if (GameManager.Instance != null && GameManager.Instance.CurrentPhase != GamePhase.Dialogue) return;
            if (choicePanel != null && choicePanel.activeSelf) return;

            // 1. Right click to toggle UI visibility (to see CG/Backgrounds)
            if (Input.GetMouseButtonDown(1))
            {
                isUiHidden = !isUiHidden;
                if (dialoguePanel != null) dialoguePanel.SetActive(!isUiHidden);
                if (autoButton != null) autoButton.gameObject.SetActive(!isUiHidden);
                if (skipButton != null) skipButton.gameObject.SetActive(!isUiHidden);
                if (backlogButton != null) backlogButton.gameObject.SetActive(!isUiHidden);
            }

            // If UI is hidden, left clicking restores it instead of advancing text
            if (isUiHidden)
            {
                if (Input.GetMouseButtonDown(0) || Input.GetKeyDown(KeyCode.Space) || Input.GetKeyDown(KeyCode.Return))
                {
                    isUiHidden = false;
                    if (dialoguePanel != null) dialoguePanel.SetActive(true);
                    if (autoButton != null) autoButton.gameObject.SetActive(true);
                    if (skipButton != null) skipButton.gameObject.SetActive(true);
                    if (backlogButton != null) backlogButton.gameObject.SetActive(true);
                }
                return;
            }

            // 2. Mouse Scroll Up to open Backlog
            if (Input.mouseScrollDelta.y > 0)
            {
                if (backlogButton != null && backlogButton.isActiveAndEnabled)
                {
                    backlogButton.onClick.Invoke();
                }
            }

            // 3. Space / Enter to advance dialogue
            if (Input.GetKeyDown(KeyCode.Space) || Input.GetKeyDown(KeyCode.Return))
            {
                OnClick();
            }
        }
'''

# Find the existing Update method and replace it
import re
text = re.sub(r'        private void Update\(\)\s*\{.*?(?=\n        public void OnClick)', update_code.strip() + '\n\n', text, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated DialogueUI Update method with QoL features')
