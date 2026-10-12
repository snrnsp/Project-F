import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    print("Nodes 0-10:")
    for node in data['nodes'][:10]:
        print(f"{node.get('speaker', '')}: {node.get('text', '')}".replace('\n', ' '))
    print("Nodes 60-70:")
    for node in data['nodes'][60:70]:
        print(f"{node.get('speaker', '')}: {node.get('text', '')}".replace('\n', ' '))
