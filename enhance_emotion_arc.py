import json, sys, os

sys.stdout.reconfigure(encoding='utf-8')
base = 'F:/Project-F/Assets/Resources/Data/Dialogues'

def load(fname):
    with open(os.path.join(base, fname), 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def save(fname, data):
    with open(os.path.join(base, fname), 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def make_node(speaker, text, cmd='', bg=''):
    return {
        "speaker": speaker, "text": text, "command": cmd,
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": bg, "choices": [], "id": 0, "nextNodeId": 0
    }

def reindex(nodes):
    for i, n in enumerate(nodes):
        n['id'] = i
        n['nextNodeId'] = i + 1 if i < len(nodes) - 1 else -1

# ============================================================
# 1. ch1_morning: 복선 심기 - 하루카의 피아노 이야기
#    의뢰 내용을 읽은 직후(node 44 "제발 도와주세요" 이후)
# ============================================================
data = load('ch1_morning.json')
nodes = data['nodes']

for i, n in enumerate(nodes):
    if n.get('speaker') == '하루카' and '제발 도와주세요' in n.get('text', ''):
        insert_at = i + 1
        new_nodes = [
            make_node(' ', '하루카가 종이를 접으며 잠시 멈칫했다.'),
            make_node('하루카', '...피아노 소리가 들리는데 아무도 없다니... 왠지 마음이 아프네요.'),
            make_node('리나', '마음이 아프다고? 무섭다가 아니고?'),
            make_node('하루카', '혼자서 아무도 없는 곳에서 계속 연주하고 있다는 거잖아요. 그게... 좀...'),
            make_node(' ', '하루카가 말끝을 흐렸다. 평소의 밝은 표정이 잠깐 어두워졌다가, 이내 다시 미소를 지었다.'),
            make_node('하루카', '아, 아무것도 아니에요! 그냥 좀 생각이 나서요!'),
        ]
        for j, nn in enumerate(new_nodes):
            nodes.insert(insert_at + j, nn)
        print('1. ch1_morning: Added Haruka piano foreshadowing after node ' + str(i))
        break

reindex(nodes)
data['nodes'] = nodes
save('ch1_morning.json', data)
print('   Saved ch1_morning.json (' + str(len(nodes)) + ' nodes)')

# ============================================================
# 2. ch1_night: 복선 자라기 - 피아노 연주 시 하루카의 반응
#    피아노가 연주될 때(EFFECT:FLASH 직후) 다른 캐릭터들은 공포, 
#    하루카만 다른 반응
# ============================================================
data = load('ch1_night.json')
nodes = data['nodes']

# Find Haruka's "엄청 추워졌어요" line
for i, n in enumerate(nodes):
    if n.get('speaker') == '하루카' and '추워졌어요' in n.get('text', ''):
        # Insert BEFORE Haruka's cold reaction
        new_nodes = [
            make_node(' ', '다들 공포에 얼어붙은 가운데 — 하루카만이 다른 표정을 하고 있었다.'),
            make_node('하루카', '...이 곡... 너무 외로운 소리예요...'),
        ]
        for j, nn in enumerate(new_nodes):
            nodes.insert(i + j, nn)
        print('2. ch1_night: Added Haruka lonely melody reaction')
        break

reindex(nodes)
data['nodes'] = nodes
save('ch1_night.json', data)
print('   Saved ch1_night.json (' + str(len(nodes)) + ' nodes)')

# ============================================================
# 3. ch1_resolution: 클라이맥스 확장
#    하루카 피아노 씬을 더 길게 + 다른 캐릭터 반응 추가
# ============================================================
data = load('ch1_resolution.json')
nodes = data['nodes']

# --- 3a: 하루카가 피아노에 다가가기 전, 세이카가 지목하는 이유 ---
for i, n in enumerate(nodes):
    if n.get('speaker') == '세이카' and '하루카, 피아노 앞에 가볼래' in n.get('text', ''):
        # Insert the reason WHY Seika picks Haruka
        new_nodes = [
            make_node(' ', '세이카가 하루카를 바라보았다. 오늘 밤 내내, 다른 누구보다 이 피아니스트의 고독을 이해하고 있었던 건 하루카였다.'),
        ]
        for j, nn in enumerate(new_nodes):
            nodes.insert(i, nn)
        print('3a. ch1_resolution: Added Seika observing Haruka')
        break

# --- 3b: 피아노 마지막 연주 후, 각 캐릭터의 반응을 확장 ---
# Find "아무도 말하지 않았다" node
for i, n in enumerate(nodes):
    if '아무도 말하지 않았다' in n.get('text', '') and '여섯 명은 그 자리에' in n.get('text', ''):
        insert_at = i + 1
        new_nodes = [
            make_node(' ', '카스미가 안경을 벗었다. 렌즈에 맺힌 것이 김인지 눈물인지, 그녀 자신도 모르는 것 같았다.'),
            make_node('카스미', '(작은 목소리로) ...언니도... 이렇게 어딘가에서 연주하고 있을까요.'),
            make_node(' ', '리리스가 노트북을 닫고, 처음으로 맨눈으로 피아노를 바라보았다.'),
            make_node('미나', '...평소처럼 가식적인 대사를 덧붙이지 않았다.\n그저 조용히 눈을 감고, 고개를 살짝 숙였다.'),
        ]
        for j, nn in enumerate(new_nodes):
            nodes.insert(insert_at + j, nn)
        print('3b. ch1_resolution: Extended character reactions after final performance')
        break

# --- 3c: 새벽 씬에서 하루카의 쿠키 복선 ---
# Find Seika's oath "네버모어의 이름에 걸고"
for i, n in enumerate(nodes):
    if n.get('speaker') == '세이카' and '네버모어의 이름에 걸고 맹세한다' in n.get('text', ''):
        # Insert Haruka's quiet action BEFORE the oath
        new_nodes = [
            make_node(' ', '그때 하루카가 주머니에서 작은 호박 쿠키를 꺼냈다. 조사를 나서기 전에 구워온 것이었다.'),
            make_node('하루카', '...이건 여기에 두고 갈게요. 혼자서 피아노 치다가 출출할 수도 있으니까.'),
            make_node(' ', '피아노 위에 작은 쿠키가 놓였다. 아무도 웃지 않았다.\n하루카의 그 소박한 행동이, 이 자리에서 할 수 있는 가장 따뜻한 위로라는 걸 모두가 알고 있었다.'),
        ]
        for j, nn in enumerate(new_nodes):
            nodes.insert(i + j, nn)
        print('3c. ch1_resolution: Added Haruka cookie foreshadowing')
        break

reindex(nodes)
data['nodes'] = nodes
save('ch1_resolution.json', data)
print('   Saved ch1_resolution.json (' + str(len(nodes)) + ' nodes)')

# ============================================================
# 4. ch1_epilogue: 쿠키 콜백 강화
#    에필로그 아침 파트에서 하루카가 쿠키를 언급
# ============================================================
data = load('ch1_epilogue.json')
nodes = data['nodes']

# Find Rina's "아 몰라!" outburst
for i, n in enumerate(nodes):
    if n.get('speaker') == '리나' and '아 몰라!' in n.get('text', ''):
        insert_at = i + 1
        new_nodes = [
            make_node('하루카', '...아, 저기, 저 어젯밤에 피아노 위에 쿠키를 하나 올려뒀었는데...'),
            make_node('리나', '뭐? 왜?'),
            make_node('하루카', '그냥... 혼자 연주하다가 배고프면 어떡하나 싶어서...'),
            make_node(' ', '잠깐의 침묵 후, 리나가 후 하고 웃었다. 카스미도 안경 너머로 살짝 미소를 지었다.'),
            make_node('리나', '...너, 진짜 바보다. 진짜로.'),
            make_node('하루카', '에...? 왜 바보예요...?'),
            make_node('리나', '바보 같아서 좋다는 뜻이야, 이 호박 덕후야.'),
        ]
        for j, nn in enumerate(new_nodes):
            nodes.insert(insert_at + j, nn)
        print('4. ch1_epilogue: Added cookie callback in morning scene')
        break

reindex(nodes)
data['nodes'] = nodes
save('ch1_epilogue.json', data)
print('   Saved ch1_epilogue.json (' + str(len(nodes)) + ' nodes)')

print('\n=== ALL EMOTIONAL FORESHADOWING & CALLBACKS APPLIED ===')
print('Seeds planted in: ch1_morning, ch1_night')
print('Blooming in: ch1_resolution')
print('Callback in: ch1_epilogue')
