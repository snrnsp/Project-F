import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch0_origin.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for i, node in enumerate(data.get('nodes', [])):
    text = node.get('text', '')
    if '1년 안에 성과를 보여라' in text:
        start_idx = max(0, i - 5)
        end_idx = min(len(data['nodes']), i + 5)
        for j in range(start_idx, end_idx):
            n = data['nodes'][j]
            bg = n.get('backgroundSprite', '')
            print(f"Node {n['id']} [{n.get('speaker', '')}]: {n.get('text', '')} | BG: {bg}")
        break
