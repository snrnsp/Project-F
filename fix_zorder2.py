import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Change the loop back to forward
text = text.replace('for (int ci = folderCount - 1; ci >= 0; ci--)', 'for (int ci = 0; ci < folderCount; ci++)')

target = '''                // ===== Folder Root =====
                GameObject folder = UIHelper.CreateUIObject("Folder_" + charNames[ci], extraRoot.transform);
                
                
                RectTransform folderRt = folder.GetComponent<RectTransform>();'''

replacement = '''                // ===== Folder Root =====
                GameObject folder = UIHelper.CreateUIObject("Folder_" + charNames[ci], extraRoot.transform);
                // Insert right after the background and shadow box!
                folder.transform.SetSiblingIndex(2);
                
                RectTransform folderRt = folder.GetComponent<RectTransform>();'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Restored forward loop and used SetSiblingIndex(2)')
else:
    print('Target not found')
