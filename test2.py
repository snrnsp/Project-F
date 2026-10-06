import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for node in data['nodes'][:20]:
    speaker = node.get('speaker', '')
    text = node.get('text', '').replace('\n', ' ')
    print(f'Node {node["id"]}: [{speaker}] {text}')
