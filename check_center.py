import json
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data.get('nodes', []):
    if n['id'] < 10 and n.get('characterSpriteCenter'):
        print(f"Node {n['id']} Center: {n.get('characterSpriteCenter')}")
