import json
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)['nodes']

for i in range(23, 29):
    n = data[i]
    print(f"{n['id']}: L={n.get('characterSpriteLeft')}, C={n.get('characterSpriteCenter')}, R={n.get('characterSpriteRight')}")
