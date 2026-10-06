import json
with open('Assets/Resources/Data/Dialogues/ch1_morning.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for node in data['nodes'][:15]:
    L = node.get('characterSpriteLeft', '')
    C = node.get('characterSpriteCenter', '')
    R = node.get('characterSpriteRight', '')
    print(f"Node {node['id']}: [{node.get('speaker', '')}] L:'{L}', C:'{C}', R:'{R}'")
