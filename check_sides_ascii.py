import json
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)['nodes']
for i in range(5, 30):
    n = data[i]
    left = n.get('characterSpriteLeft', '')
    right = n.get('characterSpriteRight', '')
    if '카스미' in left or '세이카' in left or '카스미' in right or '세이카' in right:
        line = f"Node {n['id']}: L={left}, C={n.get('characterSpriteCenter', '')}, R={right}"
        print(line.encode('ascii', 'backslashreplace').decode('ascii'))
