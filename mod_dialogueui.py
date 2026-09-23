import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add flashbackOverlay field
target_field = '        [SerializeField] private Image backgroundImage;'
replacement_field = '        [SerializeField] private Image backgroundImage;\n        [SerializeField] private GameObject flashbackOverlay;'
if 'private GameObject flashbackOverlay;' not in text:
    text = text.replace(target_field, replacement_field)

# 2. Add SetFlashback method
target_method = '''        public void UpdateUI(DialogueNode node, string speakerName, string fullText, bool usePanel = true)'''
replacement_method = '''        public void SetFlashback(bool active)
        {
            if (flashbackOverlay != null) flashbackOverlay.SetActive(active);
        }

        public void UpdateUI(DialogueNode node, string speakerName, string fullText, bool usePanel = true)'''
if 'public void SetFlashback' not in text:
    text = text.replace(target_method, replacement_method)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated DialogueUI.cs with flashback support')
