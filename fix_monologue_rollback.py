import sys

path = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'bool usePanel = true;' in line and 'User requested that monologues always use the dialogue panel' in lines[i-1]:
        lines[i-1] = '            // Rule: Monologues with a background image use the dialogue panel.\n'
        lines[i] = '            bool usePanel = !isNarrator;\n'
        break

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("DialogueUI rolled back to usePanel = !isNarrator")
