import json
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)['nodes']
for n in data:
    if n['id'] == 25:
        print("L:", repr(n.get("characterSpriteLeft")))
        print("C:", repr(n.get("characterSpriteCenter")))
        print("R:", repr(n.get("characterSpriteRight")))
