import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()
for i, line in enumerate(text.split('\n')):
    if '"Portrait"' in line:
        for j in range(max(0, i-2), i+15):
            print(f'{j+1}: {text.split(chr(10))[j]}')
        break
