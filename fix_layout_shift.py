import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''            int n = _tempPositionList.Count;
            for (int i = 0; i < n; i++)
            {
                float targetX = 0.5f; // Default: center
                if (n == 2) targetX = (i == 0) ? 0.34f : 0.78f;
                else if (n == 3) targetX = (i == 0) ? 0.24f : (i == 1 ? 0.56f : 0.88f);

                CharacterPosition pos = _tempPositionList[i];
                MoveCharacterTo(pos, targetX);
            }'''

replacement = '''            int n = _tempPositionList.Count;
            for (int i = 0; i < n; i++)
            {
                float targetX = 0.5f; // Default: center
                if (n == 2) targetX = (i == 0) ? 0.25f : 0.75f;
                else if (n == 3) targetX = (i == 0) ? 0.20f : (i == 1 ? 0.50f : 0.80f);

                CharacterPosition pos = _tempPositionList[i];
                MoveCharacterTo(pos, targetX);
            }'''

target_win = target.replace('\n', '\r\n')
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated layout positions (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated layout positions (lf)')
else:
    print('Target not found')
