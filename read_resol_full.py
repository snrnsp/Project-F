import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    print("Total nodes:", len(data['nodes']))
    for i, node in enumerate(data['nodes']):
        if i > 70:
            print(f"[{node['id']}] {node.get('speaker', '')}: {node.get('text', '')}".replace('\n', ' '))
