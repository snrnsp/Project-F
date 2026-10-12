import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    print("Nodes 0-5:")
    for node in data['nodes'][:5]:
        print(f"{node.get('speaker', '')}: {node.get('text', '')}".replace('\n', ' '))
    print("Nodes 20-27:")
    for node in data['nodes'][20:28]:
        print(f"{node.get('speaker', '')}: {node.get('text', '')}".replace('\n', ' '))
