with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'rb') as f:
    text = f.read().decode('utf-8-sig', errors='replace')
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'void CreateDialogueUI' in line:
        for j in range(i, i+30):
            print(lines[j].strip().encode('ascii', 'backslashreplace').decode('ascii'))
        break
