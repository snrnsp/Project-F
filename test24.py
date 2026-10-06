import json
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for i, node in enumerate(data.get('nodes', [])):
    text = node.get('text', '')
    if '기억상실 환자의 과대망상이네요' in text:
        start_idx = max(0, i - 5)
        end_idx = min(len(data['nodes']), i + 5)
        for j in range(start_idx, end_idx):
            n = data['nodes'][j]
            L = n.get('characterSpriteLeft', '')
            C = n.get('characterSpriteCenter', '')
            R = n.get('characterSpriteRight', '')
            print(f"Node {n['id']} [{n.get('speaker', '')}]: L:'{L}', C:'{C}', R:'{R}'")
        break
