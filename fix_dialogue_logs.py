import json, os, sys
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
total_fixes = 0

# ═══════════════════════════════════════════════════════════
# 1. ch0_gathering.json — 장문 내레이션 줄바꿈 (9건)
# ═══════════════════════════════════════════════════════════
path = f'{base}/ch0_gathering.json'
data = load_json(path)
fixes = {
    1: '그런데 구시가지에서 또다시 실종 사건이 발생했다.\n\n5년 주기의 패턴. 다음 실종이 일어날 시기가 바로 올해였다.',
    5: '경찰청 과학수사대 인턴.\n\n어린 시절 사라진 언니를 찾기 위해 수사의 길을 택했지만, \'설명할 수 없는 현장\'을 무조건 덮는 관행에 지쳐 있었다.',
    15: '온라인에서 「유령 드론(GhostDrone)」이라는 이름으로 활동하던 프리랜서 해커.\n\n자작 드론으로 구시가지를 촬영하다가, 30년간 비어있는 폐건물에서 있을 수 없는 열원을 포착했다.',
    18: '이후 3층 다락방을 자신의 작업실로 개조하여 입주.\n\n정찰 드론 「잭오(Jack-O)」가 만들어진 것도 이 시기였다.',
    20: '가장 미스터리한 합류.\n\n어느 비 오는 밤, 저택 현관 앞에 쓰러져 있는 채로 발견되었다.\n\n신원 불명. 이름이 \'미나\'라는 것 외에는 아무것도 기억나지 않는다고 주장했다.',
    23: '하지만 미나에게는 설명할 수 없는 능력이 있었다.\n\n한 번도 가보지 않은 폐건물의 구조를 알고, 사건의 결말을 예언하듯 중얼거리면, 그것이 맞았다.',
    26: '구시가지의 작은 카페에서 아르바이트를 하던 19세 소녀.\n\n학교에서 심한 따돌림을 당해 자퇴한 뒤, 혼자서 생계를 유지하고 있었다.',
    30: '불과 3개월 남짓한 시간 동안, 다섯 명이 연달아 합류했다.\n\n실종 사건이라는 파장이 각자의 삶에 금을 내면서, 갈 곳 없는 사람들이 같은 장소로 흘러들어온 것이다.',
    34: '부모님이 준 1년의 기한.\n\n그 마감 직전에 기적처럼 팀이 갖춰졌다.\n\n경찰이 닫아버린 파일을 다시 여는 사람들. 세상이 외면한 것들을 마주하는 사람들.',
}
for node in data['nodes']:
    if node['id'] in fixes:
        node['text'] = fixes[node['id']]
        total_fixes += 1
save_json(path, data)
print(f'✅ ch0_gathering.json: {len(fixes)}건 줄바꿈 추가')

# ═══════════════════════════════════════════════════════════
# 2. ch0_opening.json — 장문 내레이션 줄바꿈 (3건)
# ═══════════════════════════════════════════════════════════
path = f'{base}/ch0_opening.json'
data = load_json(path)
fixes = {
    1: '인구 80만의 항구도시.\n\n낮에는 평범한 사람들이 평범한 하루를 보내고, 밤에는 바다에서 밀려온 안개가 구시가지의 좁은 골목을 채운다.',
    6: '경찰은 그것을 \'소음 민원\', \'방향감각 상실\', \'빛의 착시\'라고 처리한다.\n\n대부분의 시민들도 도시전설 정도로 여기고 넘긴다.',
    9: '현관 계단을 따라 늘어선 잭오랜턴들.\n\n처마에 걸린 거미줄 장식. 벽을 타고 오른 덩굴 사이로 깜빡이는 주황빛.',
}
for node in data['nodes']:
    if node['id'] in fixes:
        node['text'] = fixes[node['id']]
        total_fixes += 1
save_json(path, data)
print(f'✅ ch0_opening.json: {len(fixes)}건 줄바꿈 추가')

# ═══════════════════════════════════════════════════════════
# 3. ch0_origin.json — 장문 내레이션 + 장문 대사 (4건)
# ═══════════════════════════════════════════════════════════
path = f'{base}/ch0_origin.json'
data = load_json(path)
fixes = {
    9: '실종 사건을 혼자 조사하던 세이카는 모든 사건의 중심에 있는 장소를 찾아냈다.\n\n구시가지 언덕 꼭대기의 \'이케다 저택\'.',
    19: '로펌 취직을 포기하고, 전 재산과 가족 자금을 투입해 저택을 매입.\n\n1년에 걸친 리모델링 끝에 현관에 새로운 간판이 걸렸다.',
    21: '할로윈 장식은 반은 내 취향이지만, 나머지 반은 전략이야.\n\'설명할 수 없는 일\'을 겪은 사람이 편하게 찾아올 수 있는 분위기를 만들기 위해서.',
}
for node in data['nodes']:
    if node['id'] in fixes:
        node['text'] = fixes[node['id']]
        total_fixes += 1
    # 노드 2: 세이카 103자 → 2개 노드로 분할이 이상적이지만, 
    # 줄바꿈으로 우선 해결
    if node['id'] == 2:
        node['text'] = '......이상하다.\n\n노을시 구시가지 실종 사건... 2003년, 2008년, 2014년, 2019년.\n\n5년 간격으로 실종자가 발생하는데, 전부 수사 중단. 기록이 거의 남아있지 않아.'
        total_fixes += 1
save_json(path, data)
print(f'✅ ch0_origin.json: 4건 줄바꿈/분할')

# ═══════════════════════════════════════════════════════════
# 4. ch1_morning.json — 장문 내레이션 (1건) + 장문 대사 (1건)
# ═══════════════════════════════════════════════════════════
path = f'{base}/ch1_morning.json'
data = load_json(path)
fixes = {
    1: '호박 램프의 불빛이 은은하게 켜진 사무소 안.\n\n벽난로에서 장작이 타닥거리고, 거미줄 장식 사이로 아침 햇살이 비친다.',
    43: '(종이를 펼치며) \'매일 밤 3시경, 폐쇄된 음악실에서 피아노 소리가 들립니다.\n경찰에 신고했지만, 건물 내부에 아무도 없었다고 합니다.\'',
}
for node in data['nodes']:
    if node['id'] in fixes:
        node['text'] = fixes[node['id']]
        total_fixes += 1
save_json(path, data)
print(f'✅ ch1_morning.json: {len(fixes)}건 줄바꿈 추가')

# ═══════════════════════════════════════════════════════════
# 5. ch1_night.json — 장문 내레이션 (3건)
# ═══════════════════════════════════════════════════════════
path = f'{base}/ch1_night.json'
data = load_json(path)
fixes = {
    8: '일행은 노을시 외곽의 버려진 건물에 도착했다.\n\n오래된 덩굴이 외벽을 감싸고 있고, 깨진 창문 틈으로 차가운 바람이 새어나왔다.',
    13: '안으로 들어서자 짙은 먼지 냄새가 코를 찔렀다.\n\n낡은 연습실들이 늘어서 있고, 바닥에는 악보들이 어지럽게 흩어져 있었다.',
    17: '일행은 마침내 메인 공연장에 다다랐다.\n\n중앙에는 먼지 쌓인 천으로 덮인 그랜드 피아노가 덩그러니 놓여 있었다.',
}
for node in data['nodes']:
    if node['id'] in fixes:
        node['text'] = fixes[node['id']]
        total_fixes += 1
save_json(path, data)
print(f'✅ ch1_night.json: {len(fixes)}건 줄바꿈 추가')

# ═══════════════════════════════════════════════════════════
# 6. ch1_investigation_talk.json — 장문 대사 (2건)
# ═══════════════════════════════════════════════════════════
path = f'{base}/ch1_investigation_talk.json'
data = load_json(path)
fixes = {
    5: '맞습니다. 먼지 위에 선명한 발자국이 피아노를 향하고 있었는데,\n약 2미터 전에서 갑자기 사라졌습니다.\n\n걸어가던 존재가 중간에 소멸한 것처럼.',
    10: '그렇습니다. 잉크가 번진 흔적을 보면 단순한 시간의 흐름에 의한 훼손이 아닙니다.\n\n누군가 고의로... 혹은 알 수 없는 현상에 의해 그 사람의 존재 자체가 지워진 것처럼 보입니다.',
    11: '부서진 메트로놈과 낡은 음악 잡지도 수거했습니다.\n\n모든 증거의 연관성은 아직 단정 지을 수 없으니, 추리 단계에서 신중하게 판단해야 할 것입니다.',
}
for node in data['nodes']:
    if node['id'] in fixes:
        node['text'] = fixes[node['id']]
        total_fixes += 1
save_json(path, data)
print(f'✅ ch1_investigation_talk.json: {len(fixes)}건 줄바꿈 추가')

# ═══════════════════════════════════════════════════════════
# 7. ch1_result_perfect.json — 장문 대사 + 말투 수정 (3건)
# ═══════════════════════════════════════════════════════════
path = f'{base}/ch1_result_perfect.json'
data = load_json(path)
fixes = {
    4: '바닥의 발자국은 피아노를 향해 걸어갔지만 도중에 사라졌어.\n\n걸어가던 존재가 소멸한 거야. 물리적으로 이 공간에 있었다가 사라졌다는 움직일 수 없는 증거지.',
    8: '......과학적으로 말이 안 됩니다. 하지만... 증거가 그렇게 가리키고 있으니 인정할 수밖에 없습니다.',
    17: '피아노는 이제 침묵하고 있지만, 모두가 알고 있었다.\n\n그곳에 여전히 누군가 남아 기억되기를 기다리고 있다는 것을.',
}
for node in data['nodes']:
    if node['id'] in fixes:
        node['text'] = fixes[node['id']]
        total_fixes += 1
save_json(path, data)
print(f'✅ ch1_result_perfect.json: {len(fixes)}건 (줄바꿈 + 말투 수정)')

print(f'\n═══ 전체 수정 완료: 총 {total_fixes}건 ═══')
