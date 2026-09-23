import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/Dialogue/DialogueManager.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            // Handle flashback visuals for specific past stories
            if (dialogueUI != null)
            {
                bool isFlashback = container.dialogueId == "ch0_origin" || container.dialogueId == "ch0_gathering";
                dialogueUI.SetFlashback(isFlashback);
            }'''

text = text.replace(target, '')

# Add CurrentDialogueId property so DialogueUI can read it
if 'public string CurrentDialogueId' not in text:
    prop_target = '        private DialogueContainer currentDialogue;'
    prop_repl = '        private DialogueContainer currentDialogue;\n        public string CurrentDialogueId => currentDialogue?.dialogueId;'
    text = text.replace(prop_target, prop_repl)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed DialogueManager.cs')
