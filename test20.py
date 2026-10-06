import json
with open('Assets/Resources/Data/Dialogues/ch1_morning.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    if '\n' in node.get('text', ''):
        print(f"Node {node['id']} [{node.get('speaker', '')}]: has newline")
