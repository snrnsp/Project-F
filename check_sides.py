import json
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)['nodes']

for i in range(5, 30):
    n = data[i]
    if '카스미' in n.get('characterSpriteLeft', '') or '세이카' in n.get('characterSpriteLeft', ''):
        print(f"Node {n['id']}: L={n.get('characterSpriteLeft')}, C={n.get('characterSpriteCenter')}, R={n.get('characterSpriteRight')}")
