with open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'rb') as f:
    text = f.read().decode('utf-8-sig', errors='replace')
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'target +=' in line or 'target -=' in line:
        print(f'{i-3}: {lines[i-3].strip().encode("ascii", "backslashreplace").decode("ascii")}')
        print(f'{i-2}: {lines[i-2].strip().encode("ascii", "backslashreplace").decode("ascii")}')
        print(f'{i-1}: {lines[i-1].strip().encode("ascii", "backslashreplace").decode("ascii")}')
        break
