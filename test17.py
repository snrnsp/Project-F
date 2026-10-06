import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch1_resolution.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes'][90:105]:
    L = node.get('characterSpriteLeft', '')
    C = node.get('characterSpriteCenter', '')
    R = node.get('characterSpriteRight', '')
    print(f"Node {node['id']} [{node.get('speaker', '')}]: L:'{L}', C:'{C}', R:'{R}'")
