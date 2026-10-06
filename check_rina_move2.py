import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for i in range(5, 22):
    n = data['nodes'][i]
    L = n.get('characterSpriteLeft', '')
    C = n.get('characterSpriteCenter', '')
    R = n.get('characterSpriteRight', '')
    print(f"Node {n['id']} [{n.get('speaker', '')}]: L='{L}', C='{C}', R='{R}'")
