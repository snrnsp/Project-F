import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')
with codecs.open('F:/Project-F/Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

in_func = False
start_idx = -1
for i, line in enumerate(lines):
    if 'void UpdateVisualsOnly' in line:
        start_idx = i
        break

if start_idx != -1:
    end_idx = start_idx + 180
    for line in lines[start_idx:end_idx]:
        print(line.rstrip('\r\n'))
