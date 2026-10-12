import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/BacklogUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'''            history\.Add\(new BacklogEntry\(currentDialogId, node\)\);\r?\n\s*if \(history\.Count > 100\)\r?\n\s*\{\r?\n\s*history\.RemoveAt\(0\);\r?\n\s*\}'''
replacement = r'''            history.Add(new BacklogEntry(currentDialogId, node));
            if (history.Count > 300)
            {
                history.RemoveAt(0);
            }'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed history cap in BacklogUI!")
else:
    print("Failed to match history cap in BacklogUI!")
