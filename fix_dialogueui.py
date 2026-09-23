import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        public void UpdateUI(DialogueNode node, string speakerName, string fullText, bool usePanel = true)
        {
            if (node == null) return;'''

replacement = '''        public void UpdateUI(DialogueNode node, string speakerName, string fullText, bool usePanel = true)
        {
            if (node == null) return;
            
            if (DialogueManager.Instance != null)
            {
                string id = DialogueManager.Instance.CurrentDialogueId;
                SetFlashback(id == "ch0_origin" || id == "ch0_gathering");
            }'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated DialogueUI to check flashback state')
