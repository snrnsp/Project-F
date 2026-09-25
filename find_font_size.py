import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()
lines = text.split('\n')
for i, line in enumerate(lines):
    if '"NameText"' in line or '"DescText"' in line or '"Profile"' in line:
        pass
        
for i, line in enumerate(lines):
    if 'infoPanelObj' in line:
        for j in range(max(0, i-2), min(len(lines), i+40)):
            print(f'{j+1}: {lines[j]}')
        break
