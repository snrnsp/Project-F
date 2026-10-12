import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_result_perfect.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    speaker = str(node.get('speaker', '')).strip()
    if not speaker:
        print(f"Node {node['id']}: {node['text']}")
