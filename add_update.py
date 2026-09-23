import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

update_code = '''
        private void Update()
        {
            if (GameManager.Instance != null && GameManager.Instance.CurrentPhase != GamePhase.Dialogue) return;
            if (choicePanel != null && choicePanel.activeSelf) return;

            if (Input.GetKeyDown(KeyCode.Space) || Input.GetKeyDown(KeyCode.Return))
            {
                OnClick();
            }
        }
'''

text = text.replace('public void OnClick()', update_code + '\n        public void OnClick()')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added Update method to DialogueUI.cs')
