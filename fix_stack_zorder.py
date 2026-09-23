import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''            // Update folder visuals and Z-order
            for (int i = 0; i < folderObjects.Count; i++)
            {
                bool isSelected = (i == index);
                GameObject folder = folderObjects[i];
                RectTransform rt = folder.GetComponent<RectTransform>();

                if (isSelected)
                {
                    // Bring selected folder to front
                    folder.transform.SetAsLastSibling();
                    
                    // Move to center/active position'''

replacement = '''            // First, correct the Z-order for unselected folders to maintain the stack
            for (int i = 0; i < folderObjects.Count; i++)
            {
                if (i != index)
                {
                    // Insert at index 2 (right after background/shadow).
                    // As we iterate 0->5, later folders push earlier ones forward.
                    // This perfectly restores the 5->0 depth order for the unselected stack!
                    folderObjects[i].transform.SetSiblingIndex(2);
                }
            }
            // Bring selected folder to the front of the folder stack (but behind Header/CloseBtn)
            if (folderObjects.Count > 0)
                folderObjects[index].transform.SetSiblingIndex(2 + folderObjects.Count - 1);

            // Update folder visuals
            for (int i = 0; i < folderObjects.Count; i++)
            {
                bool isSelected = (i == index);
                GameObject folder = folderObjects[i];
                RectTransform rt = folder.GetComponent<RectTransform>();

                if (isSelected)
                {
                    // Move to center/active position'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Fixed Z-order restoration and prevented covering Header/CloseBtn')
else:
    print('Target not found')
