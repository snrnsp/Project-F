import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')
with codecs.open('F:/Project-F/Assets/Scripts/UI/BacklogUI.cs', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

start_idx = -1
for i, line in enumerate(lines):
    if 'private void OnEntryClicked' in line:
        start_idx = i
        break

if start_idx != -1:
    for j in range(start_idx, start_idx+30):
        if j < len(lines):
            print(lines[j].rstrip('\r\n'))
