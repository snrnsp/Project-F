import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'UIHelper.SetField(ui, \"autoButtonText\"' in line or 'CreateDialogueUI' in line:
        start = max(0, i - 15)
        end = min(len(lines), i + 20)
        print(f"--- Line {i} ---")
        for j in range(start, end):
            print(f"{j}: {lines[j].strip()}")
        break
