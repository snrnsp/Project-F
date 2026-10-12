import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    if node['id'] in [96, 97, 98]:
        print(f"[{node['id']}] {node.get('text', '')}".replace('\n', ' '))
