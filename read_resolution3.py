import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    print("Nodes 10-30:")
    for node in data['nodes'][10:30]:
        print(f"{node.get('speaker', '')}: {node.get('text', '')}".replace('\n', ' '))
