import json
import glob

files = glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json')
long_lines = []

for filepath in files:
    if '_legacy' in filepath: continue
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    nodes = data.get('nodes', [])
    for i, node in enumerate(nodes):
        text = node.get('text', '')
        for line in text.split('\n'):
            if len(line) > 95:
                long_lines.append(f"[{filepath.split('/')[-1]}] Node {node.get('id', i)}: {len(line)} chars")

for ll in long_lines:
    print(ll)
print(f"Total long lines: {len(long_lines)}")
