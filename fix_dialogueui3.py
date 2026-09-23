import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        public void DisplayNode(DialogueNode node)'''
replacement = '''        public void SetFlashback(bool active)
        {
            if (flashbackOverlay != null) flashbackOverlay.SetActive(active);
        }

        public void DisplayNode(DialogueNode node)'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added SetFlashback to DialogueUI')
