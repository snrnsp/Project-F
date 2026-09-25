import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'Haruka' in line or '하루카' in line:
        for j in range(max(0, i-2), i+15):
            print(f'{j+1}: {lines[j]}')
        break
