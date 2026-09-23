import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'private (UnityEngine.UI.Button btn, Text legacyText) CreateLegacyButton' in line:
        start = max(0, i - 5)
        end = min(len(lines), i + 20)
        for j in range(start, end):
            print(f"{j}: {lines[j].strip().encode('ascii', 'backslashreplace').decode('ascii')}")
        break
