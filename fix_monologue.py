import sys

path = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'bool usePanel = !isNarrator;' in line:
        lines[i] = '            // User requested that monologues always use the dialogue panel without a speaker\n            bool usePanel = true;\n'
        break

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("DialogueUI updated to use dialogue panel for monologues")
