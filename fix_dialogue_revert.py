import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def load_json(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        raw = f.read()
        while raw.startswith('\ufeff'):
            raw = raw[1:]
        return json.loads(raw)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

base = 'F:/Project-F/Assets/Resources/Data/Dialogues'
total = 0

# ═══ 대사 노드(speaker가 있는 노드)에서 \n\n 줄바꿈 원복 ═══

# 1. ch0_origin.json — 노드 2 (세이카), 노드 21 (세이카)
path = f'{base}/ch0_origin.json'
data = load_json(path)
for node in data['nodes']:
    if node['id'] == 2:
        node['text'] = '......이상하다. 노을시 구시가지 실종 사건... 2003년, 2008년, 2014년, 2019년. 5년 간격으로 실종자가 발생하는데, 전부 수사 중단. 기록이 거의 남아있지 않아.'
        total += 1
    if node['id'] == 21:
        node['text'] = '할로윈 장식은 반은 내 취향이지만, 나머지 반은 전략이야. \'설명할 수 없는 일\'을 겪은 사람이 편하게 찾아올 수 있는 분위기를 만들기 위해서.'
        total += 1
save_json(path, data)
print(f'✅ ch0_origin.json: 대사 노드 2건 원복')

# 2. ch1_morning.json — 노드 43 (하루카)
path = f'{base}/ch1_morning.json'
data = load_json(path)
for node in data['nodes']:
    if node['id'] == 43:
        node['text'] = '(종이를 펼치며) \'매일 밤 3시경, 폐쇄된 음악실에서 피아노 소리가 들립니다. 경찰에 신고했지만, 건물 내부에 아무도 없었다고 합니다.\''
        total += 1
save_json(path, data)
print(f'✅ ch1_morning.json: 대사 노드 1건 원복')

# 3. ch1_investigation_talk.json — 노드 5, 10, 11 (카스미)
path = f'{base}/ch1_investigation_talk.json'
data = load_json(path)
for node in data['nodes']:
    if node['id'] == 5:
        node['text'] = '맞습니다. 먼지 위에 선명한 발자국이 피아노를 향하고 있었는데, 약 2미터 전에서 갑자기 사라졌습니다. 걸어가던 존재가 중간에 소멸한 것처럼.'
        total += 1
    if node['id'] == 10:
        node['text'] = '그렇습니다. 잉크가 번진 흔적을 보면 단순한 시간의 흐름에 의한 훼손이 아닙니다. 누군가 고의로... 혹은 알 수 없는 현상에 의해 그 사람의 존재 자체가 지워진 것처럼 보입니다.'
        total += 1
    if node['id'] == 11:
        node['text'] = '부서진 메트로놈과 낡은 음악 잡지도 수거했습니다. 모든 증거의 연관성은 아직 단정 지을 수 없으니, 추리 단계에서 신중하게 판단해야 할 것입니다.'
        total += 1
save_json(path, data)
print(f'✅ ch1_investigation_talk.json: 대사 노드 3건 원복')

# 4. ch1_result_perfect.json — 노드 4 (세이카)
path = f'{base}/ch1_result_perfect.json'
data = load_json(path)
for node in data['nodes']:
    if node['id'] == 4:
        node['text'] = '바닥의 발자국은 피아노를 향해 걸어갔지만 도중에 사라졌어. 걸어가던 존재가 소멸한 거야. 물리적으로 이 공간에 있었다가 사라졌다는 움직일 수 없는 증거지.'
        total += 1
save_json(path, data)
print(f'✅ ch1_result_perfect.json: 대사 노드 1건 원복')

print(f'\n═══ 총 {total}건 대사 노드 원복 완료 ═══')
print('(내레이션 노드의 줄바꿈은 그대로 유지)')
