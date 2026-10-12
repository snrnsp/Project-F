import json

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for i in range(25, 30):
    n = data['nodes'][i]
    print(f"Node {i} | Speaker: {n.get('speaker', '')} | Mina(C): {n.get('characterSpriteCenter', '')}")
