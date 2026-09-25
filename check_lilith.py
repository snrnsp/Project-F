import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    speaker = node.get('speaker', '')
    left = node.get('characterSpriteLeft', '')
    center = node.get('characterSpriteCenter', '')
    right = node.get('characterSpriteRight', '')
    default = node.get('characterSprite', '')
    
    if '작업실이 필요했는데' in node.get('text', ''):
        print(f"Node {node['id']}: Speaker: {speaker} | L: {left} | C: {center} | R: {right} | Def: {default}")
