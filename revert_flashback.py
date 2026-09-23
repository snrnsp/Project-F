import codecs
import re

# 1. Revert HalloweenUIBuilder
path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the Flashback Overlay creation
start_str = '            // Flashback Overlay (between characters and dialogue panel)'
end_str = '            // Dialogue Panel'
if start_str in text and end_str in text:
    idx1 = text.find(start_str)
    idx2 = text.find(end_str)
    text = text[:idx1] + text[idx2:]

text = text.replace('UIHelper.SetField(ui, "flashbackOverlay", dialoguePanelRoot.transform.Find("FlashbackOverlay").gameObject);', '')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

# 2. Revert DialogueUI
path2 = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path2, 'r', encoding='utf-8') as f:
    text2 = f.read()

text2 = text2.replace('        [SerializeField] private GameObject flashbackOverlay;', '')
text2 = re.sub(r'        public void SetFlashback\(bool active\)\s*\{\s*if \(flashbackOverlay != null\) flashbackOverlay\.SetActive\(active\);\s*\}', '', text2)
text2 = text2.replace('''            if (DialogueManager.Instance != null)
            {
                string id = DialogueManager.Instance.CurrentDialogueId;
                SetFlashback(id == "ch0_origin" || id == "ch0_gathering");
            }''', '')

with open(path2, 'w', encoding='utf-8-sig') as f:
    f.write(text2)

print('Reverted FlashbackOverlay from UI code')
