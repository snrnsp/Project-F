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
# Fix 1: ch0_gathering node 4 "실종 발생 직후" → "실종 징후 포착 직후"
# ============================================================
data = load('ch0_gathering.json')
for n in data['nodes']:
    if '실종 발생 직후' in n.get('text', ''):
        n['text'] = n['text'].replace('실종 발생 직후', '실종 징후 포착 직후')
        print('Fix 1: 실종 발생 -> 징후 포착 (node ' + str(n['id']) + ')')
save('ch0_gathering.json', data)

# ============================================================
# Fix 2: 음계 암호 → 모스 부호(장단음) 방식으로 전면 변경
#   피아니스트가 음의 장단으로 모스 부호를 만드는 건 직관적이고 납득됨
# ============================================================
data = load('ch1_resolution.json')
nodes = data['nodes']

# Find the decoding sequence (리리스's lines about musical cipher)
start_idx = -1
end_idx = -1
for i, n in enumerate(nodes):
    if n.get('speaker') == '리리스' and '같은 음을 의도적으로 반복해서' in n.get('text', ''):
        start_idx = i
    if n.get('speaker') == '리리스' and '나머지 음은 노이즈에 묻혀서' in n.get('text', ''):
        end_idx = i
        break

if start_idx >= 0 and end_idx >= 0:
    # Remove old decoding nodes (start_idx to end_idx inclusive)
    del nodes[start_idx:end_idx + 1]
    
    # Insert new morse code decoding sequence
    new_nodes = [
        make_node('리리스', '이 선율, 단순한 즉흥 연주가 아니야. 음의 길이가 일정한 패턴으로 반복되고 있어.'),
        make_node('카스미', '음의 길이가 패턴? 어떤 의미가 있는 건가요?'),
        make_node('리리스', '짧은 음과 긴 음이 번갈아 나와. 이건... 모스 부호야.'),
        make_node('리나', '모스 부호?! 유령이 피아노로 모스 부호를 친다고?!'),
        make_node('리리스', '피아니스트니까. 음의 장단으로 메시지를 전하는 건 오히려 자연스럽지.'),
        make_node(' ', '리리스의 손가락이 노트북 위에서 빠르게 움직였다.\n짧은 음을 점, 긴 음을 선으로 치환하자 화면에 글자가 떠올랐다.'),
        make_node('리리스', '디코딩 결과... ㅎ, ㅏ, ㅇ, ㅠ. 하유.'),
        make_node('하루카', '하유... 이름인가요?'),
        make_node('리리스', '뒷부분은 노이즈에 묻혀서 복원이 안 돼. 이름의 일부만 남은 거야.'),
    ]
    
    for j, nn in enumerate(new_nodes):
        nodes.insert(start_idx + j, nn)
    
    print('Fix 2: Replaced musical cipher with morse code (' + str(len(new_nodes)) + ' nodes)')

# ============================================================
# Fix 3: 발자국 소멸 vs 건반 물리적 누름 → 집념으로 해소
#   investigation_talk에서 카스미의 설명 보강
# ============================================================
save('ch1_resolution.json', {'dialogueId': data['dialogueId'], 'nodes': nodes})

data2 = load('ch1_investigation_talk.json')
for n in data2['nodes']:
    if '의자에 앉으려던 순간에 소멸한 것처럼' in n.get('text', ''):
        n['text'] = '선명한 발자국이 피아노를 향하고 있었는데, 의자 부근에서 갑자기 흐려지더니 사라졌습니다. 육체가 현상에 잠식당해 발자국을 남길 질량마저 잃어버린 겁니다.'
        print('Fix 3a: Footprint description updated (node ' + str(n['id']) + ')')

save('ch1_investigation_talk.json', data2)

# Also update result_perfect if it mentions physical pressing
data3 = load('ch1_result_perfect.json')
for n in data3['nodes']:
    if '물리적으로' in n.get('text', '') and '피아노를 쳤다는 증거' in n.get('text', ''):
        n['text'] = n['text'].replace(
            '누군가 물리적으로 이곳에서 피아노를 쳤다는 증거지.',
            '존재가 지워져가면서도 오직 집념 하나로 건반을 누르고 있었다는 증거지.'
        )
        print('Fix 3b: Physical playing -> obsession-driven (node ' + str(n['id']) + ')')
save('ch1_result_perfect.json', data3)

# ============================================================
# Fix 4: 온도 "5도 이상" → "영하권" (8월에 5도 하락은 약함)
# ============================================================
data2 = load('ch1_investigation_talk.json')
for n in data2['nodes']:
    if '온도만 5도 이상 급격히 떨어졌어' in n.get('text', ''):
        n['text'] = n['text'].replace('온도만 5도 이상 급격히 떨어졌어', '한여름인데 피아노 주변 온도가 영하권까지 떨어졌어')
        print('Fix 4: 5도 -> 영하권 (node ' + str(n['id']) + ')')
save('ch1_investigation_talk.json', data2)

# Also fix in ch1_night if the temperature line is there
data_night = load('ch1_night.json')
for n in data_night['nodes']:
    if n.get('speaker') == '리리스' and '온도' in n.get('text', '') and '5도' in n.get('text', ''):
        n['text'] = n['text'].replace('5도', '영하권까지')
        print('Fix 4b: ch1_night temperature fixed (node ' + str(n['id']) + ')')
save('ch1_night.json', data_night)

# ============================================================
# Fix 5: Reindex ch1_resolution
# ============================================================
data = load('ch1_resolution.json')
reindex(data['nodes'])
save('ch1_resolution.json', data)
print('Reindexed ch1_resolution.json (' + str(len(data['nodes'])) + ' nodes)')

print('\nAll fixes applied!')
