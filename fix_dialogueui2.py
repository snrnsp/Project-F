import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        public void DisplayNode(DialogueNode node)
        {
            if (speakerNameText != null) speakerNameText.text = node.speaker;'''

replacement = '''        public void DisplayNode(DialogueNode node)
        {
            if (DialogueManager.Instance != null)
            {
                string id = DialogueManager.Instance.CurrentDialogueId;
                SetFlashback(id == "ch0_origin" || id == "ch0_gathering");
            }
            if (speakerNameText != null) speakerNameText.text = node.speaker;'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated DisplayNode to activate flashback tint')
