import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    print("Total nodes:", len(data['nodes']))
    for node in data['nodes'][:15]:
        print(f"[{node['id']}] {node.get('speaker', '')}: {node.get('text', '')}".replace('\n', ' '))
