import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                        if (node.slideIn)
                        {
                            // Start from center, then slide to target
                            SetCharacterAnchorX(rt, 0.5f);
                            MoveCharacterTo(assignedPos, targetX);
                        }
                        else
                        {
                            SetCharacterAnchorX(rt, targetX);
                        }'''

replacement = '''                        bool isFirst = _activeSpeakerPositions.Count == 1;
                        if (node.slideIn || !isFirst)
                        {
                            // Start from center, then slide to target outwards with existing characters
                            SetCharacterAnchorX(rt, 0.5f);
                            MoveCharacterTo(assignedPos, targetX);
                        }
                        else
                        {
                            SetCharacterAnchorX(rt, targetX);
                        }'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated new character sliding logic in DialogueUI')
else:
    print('Target not found in DialogueUI')
