filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(80, min(100, len(lines))):
    print(str(i+1) + ': ' + lines[i].rstrip())
