import json
with open('Assets/Resources/Data/Dialogues/ch1_resolution.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', [])[100:110]:
    print(f"Node {node['id']} [{node.get('speaker', '')}]: {repr(node.get('text', ''))}")
