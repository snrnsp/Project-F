import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

start_idx = text.find('            // Apply visual offsets for sprites that have off-center bodies')
end_idx = text.find('            // Now assign positions and place characters')

if start_idx != -1 and end_idx != -1:
    text = text[:start_idx] + text[end_idx:]
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Removed the visual offsets block.")
else:
    print("Could not find the block.")
