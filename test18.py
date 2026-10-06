import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    speaker = node.get('speaker', '').strip()
    L = node.get('characterSpriteLeft', '')
    C = node.get('characterSpriteCenter', '')
    R = node.get('characterSpriteRight', '')
    if speaker == '' and not L and not C and not R:
        print(f"Node {node['id']}: Narrator with empty sprites")
