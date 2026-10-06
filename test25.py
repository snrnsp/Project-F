import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes'][24:32]:
    print(f"Node {node['id']} [{node.get('speaker', '')}]: {node.get('text', '')}")
