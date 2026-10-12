import json

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for i in range(24, 30):
    n = data['nodes'][i]
    print(f"Node {i} | Mina: {n.get('characterSpriteCenter', '')}")
