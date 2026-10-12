import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_opening.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    text = node.get('text', '').replace('\n', ' ')
    print(f"[{node['id']}] {node.get('speaker', '')}: {text}")
