import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for i, node in enumerate(data.get('nodes', [])):
    if '놀랍게도 쓸모가 있습니다' in node.get('text', ''):
        start_idx = max(0, i - 4)
        end_idx = min(len(data['nodes']), i + 4)
        for j in range(start_idx, end_idx):
            n = data['nodes'][j]
            L = n.get('characterSpriteLeft', '')
            C = n.get('characterSpriteCenter', '')
            R = n.get('characterSpriteRight', '')
            print(f"Node {n['id']} [{n.get('speaker', '')}]: L='{L}', C='{C}', R='{R}'")
        break
