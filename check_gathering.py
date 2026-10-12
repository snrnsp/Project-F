import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes'][:15]:
    print(f"[{node['id']}] {node.get('speaker', '')}: {node.get('text', '')}")
