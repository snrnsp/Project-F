import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch1_morning.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    speaker = node.get('speaker', '').strip()
    L = node.get('characterSpriteLeft', '')
    C = node.get('characterSpriteCenter', '')
    R = node.get('characterSpriteRight', '')
    sprites = [s for s in [L, C, R] if s]
    
    if speaker and speaker not in ['서하유', '선임 변호사', '경찰', '???', '뉴스 앵커', '기자', '경찰관', '동네 할머니', '아버지']:
        found = False
        for s in sprites:
            if speaker in s:
                found = True
        if not found:
            print(f"Node {node['id']} speaker {speaker} not in {sprites}")
