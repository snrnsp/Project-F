import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/Dialogue/DialogueManager.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        public void StartDialogue(DialogueContainer container)
        {
            currentDialogue = container;
            IsPlaying = true;
            OnDialogueStarted?.Invoke();'''

replacement = '''        public void StartDialogue(DialogueContainer container)
        {
            currentDialogue = container;
            IsPlaying = true;
            OnDialogueStarted?.Invoke();
            
            // Handle flashback visuals for specific past stories
            if (dialogueUI != null)
            {
                bool isFlashback = container.dialogueId == "ch0_origin" || container.dialogueId == "ch0_gathering";
                dialogueUI.SetFlashback(isFlashback);
            }'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated DialogueManager to activate flashback tint')
