import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch0_origin.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    if not node.get('speaker', '').strip():
        print(f"Node {node['id']}: {node.get('text', '')}")
