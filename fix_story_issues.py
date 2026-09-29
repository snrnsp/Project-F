import json, sys, os

sys.stdout.reconfigure(encoding='utf-8')
base = 'F:/Project-F/Assets/Resources/Data/Dialogues'

# ============================================================
# Fix 1: Timeline - ch0_origin.json
# ============================================================
path = os.path.join(base, 'ch0_origin.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data['nodes']:
    if n['id'] == 0:
        n['text'] = '— 2025년 봄. (1년 반 전)'
    elif n['id'] == 8:
        n['text'] = '— 2025년 10월 31일, 할로윈 밤. (1년 전)'

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Fix 1: ch0_origin.json timeline corrected')

# ============================================================
# Fix 2: Phenomenon description - ch1_resolution.json
#   Soften "모조리 소멸시킨다" to "서서히 부식시킨다"
# ============================================================
path = os.path.join(base, 'ch1_resolution.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data['nodes']:
    # Find Mina's line about erasing records
    if n.get('speaker') == '미나' and '기록에서 사라지고' in n.get('text', ''):
        n['text'] = '기록이 서서히 부식되고, 기억이 흐려지고, 이름이 사라지고... 마지막에는 육체마저 투명해져.'
        print('Fix 2a: Softened Phenomenon description (records)')
    
    if n.get('speaker') == '미나' and '모든 기억과 기록마저 모조리 소멸시키는' in n.get('text', ''):
        n['text'] = '크읏... 심연의 고문서에 기록된 바와 같군. 존재뿐만 아니라 기억과 기록마저 서서히 부식시키는 \'그 현상\'...'
        print('Fix 2b: Softened Phenomenon description (Mina chuuni)')

# ============================================================
# Fix 3: Add 2021 victim mention after Kasumi's line
#   Find Kasumi's "다음 주기는... 2021년. 그리고 그 다음은 올해, 2026년." (Node 28)
#   Insert Seika's response about 2021 victim
# ============================================================
nodes = data['nodes']
insert_idx = -1
for i, n in enumerate(nodes):
    if n.get('speaker') == '카스미' and '2021년' in n.get('text', '') and '2026년' in n.get('text', ''):
        insert_idx = i + 1
        break

if insert_idx >= 0:
    new_node = {
        "id": 0,  # will be reassigned
        "speaker": "세이카",
        "text": "안타깝게도 2021년의 피해자는 아직 단서조차 찾지 못했어. 하지만 올해, 2026년의 희생자만큼은 반드시 막아야 해.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 0, "command": ""
    }
    nodes.insert(insert_idx, new_node)
    
    # Re-index all nodes
    for i, n in enumerate(nodes):
        n['id'] = i
        n['nextNodeId'] = i + 1 if i < len(nodes) - 1 else -1
    
    print('Fix 3: Added 2021 victim mention after node ' + str(insert_idx - 1))
else:
    print('Fix 3: WARNING - Could not find Kasumi 2021 line')

data['nodes'] = nodes
with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Saved ch1_resolution.json (' + str(len(nodes)) + ' nodes)')

# ============================================================
# Also check ch1_result_perfect.json for the same Mina line
# ============================================================
path = os.path.join(base, 'ch1_result_perfect.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data['nodes']:
    if n.get('speaker') == '미나' and '모든 기억과 기록마저 모조리 소멸시키는' in n.get('text', ''):
        n['text'] = '크읏... 심연의 고문서에 기록된 바와 같군. 존재뿐만 아니라 기억과 기록마저 서서히 부식시키는 \'그 현상\'...'
        print('Fix 2c: Also fixed in ch1_result_perfect.json')

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('\nAll fixes applied!')
