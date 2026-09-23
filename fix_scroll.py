import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            // 2. Mouse Scroll Up to open Backlog
            if (Input.mouseScrollDelta.y > 0)
            {
                if (backlogButton != null && backlogButton.isActiveAndEnabled)
                {
                    backlogButton.onClick.Invoke();
                }
            }'''

replacement = '''            // 2. Mouse Scroll Up to open Backlog
            if (Input.mouseScrollDelta.y > 0)
            {
                var backlog = Object.FindObjectOfType<BacklogUI>(true);
                if (backlog != null && !backlog.IsOpen)
                {
                    backlog.ShowBacklog();
                }
            }'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed scroll input in DialogueUI')
