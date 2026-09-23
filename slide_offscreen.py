import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''                        if (node.slideIn || !isFirst)
                        {
                            // Start from center, then slide to target outwards with existing characters
                            SetCharacterAnchorX(rt, 0.5f);
                            MoveCharacterTo(assignedPos, targetX);
                        }'''

replacement = '''                        if (node.slideIn || !isFirst)
                        {
                            // Start from off-screen (left or right depending on target position)
                            float offScreenX = (targetX < 0.5f) ? -0.5f : (targetX > 0.5f ? 1.5f : -0.5f);
                            SetCharacterAnchorX(rt, offScreenX);
                            MoveCharacterTo(assignedPos, targetX);
                        }'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated DialogueUI to slide new characters from off-screen')
else:
    print('Target not found')
