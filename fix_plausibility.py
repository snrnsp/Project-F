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
# Fix 1: 에필로그 기한 언급 → 구체적 "석 달"로 변경
# ============================================================
data = load('ch1_epilogue.json')
for n in data['nodes']:
    if '아버지가 준 1년' in n.get('text', '') and '절반도 안 남았어' in n.get('text', ''):
        n['text'] = '(작은 목소리로) ...아버지가 준 1년. 이제 석 달밖에 남지 않았어.'
        print('Fix 1: 절반도 안 남았어 -> 석 달 (node ' + str(n['id']) + ')')
save('ch1_epilogue.json', data)

# ============================================================
# Fix 2: 피아노 소리가 최근에야 들리기 시작한 이유 설명 추가
#   ch1_resolution에서 "2016년 피해자" 언급 직후에 추가
# ============================================================
data = load('ch1_resolution.json')
nodes = data['nodes']

for i, n in enumerate(nodes):
    if n.get('speaker') == '세이카' and '2016년 주기의 피해자일 가능성이 높아' in n.get('text', ''):
        insert_at = i + 1
        new_nodes = [
            make_node('카스미', '하지만 의문입니다. 10년 전에 사라진 사람의 연주가 왜 하필 최근 일주일 전부터 들리기 시작한 걸까요?'),
            make_node('세이카', '완전히 지워지기 직전이니까. 존재가 소멸하는 마지막 단계에서 경계가 얇아지면서, 현실로 소리가 새어나오기 시작한 거야.'),
            make_node('세이카', '역설적이지만... 이 소리가 들린다는 건, 이 사람에게 남은 시간이 얼마 없다는 뜻이야.'),
        ]
        for j, nn in enumerate(new_nodes):
            nodes.insert(insert_at + j, nn)
        print('Fix 2: Added piano timing explanation after node ' + str(i))
        break

# ============================================================
# Fix 3: 미나의 투시 → 증거 기반으로 보강 (deus ex machina 해소)
#   미나는 단편적 환영만 보고, 나머지는 증거로 뒷받침
# ============================================================
for i, n in enumerate(nodes):
    # 미나의 과도한 디테일을 줄임
    if n.get('speaker') == '미나' and '콩쿠르... 전국 콩쿠르를 앞두고 있어' in n.get('text', ''):
        n['text'] = '...무언가에 지독하게 매달리고 있어. 손가락이 피 날 때까지 건반을 치고 있어.'
        # 다음 노드(가족도 없고)도 수정
        if i + 1 < len(nodes) and '가족도 없고' in nodes[i+1].get('text', ''):
            nodes[i+1]['speaker'] = '카스미'
            nodes[i+1]['text'] = '아까 수거한 낡은 음악 잡지를 보십시오. 사진과 이름은 부식되어 판독 불가하지만, \'올해의 유망주가 전국 콩쿠르를 앞두고 있다\'는 기사 내용은 남아 있습니다. 미나가 본 환영의 정체와 일치합니다.'
            print('Fix 3: Replaced Mina deus ex machina with evidence-backed deduction')
        break

# ============================================================
# Fix 4: 음파 디코딩 → 음악적 암호(독일어 음계) 방식으로 변경
# ============================================================
for n in nodes:
    if "음파 스펙트로그램을 시각화하니까" in n.get('text', ''):
        n['text'] = '이 선율, 단순한 즉흥 연주가 아니야. 특정 음을 반복해서 치고 있어. 음악에서 쓰는 독일어 음계 표기법으로 대입하면...'
        print('Fix 4a: Changed spectrogram to musical cipher (node ' + str(n['id']) + ')')
    if "'하... 유...' 나머지는 노이즈에 묻혀서 복원이 안 돼." in n.get('text', ''):
        n['text'] = "H, A, Y, U... '하유'. 나머지 음은 노이즈에 묻혀서 복원이 안 돼."
        print('Fix 4b: Changed to HAYU musical notation (node ' + str(n['id']) + ')')

# ============================================================
# Fix 5: 카스미의 감정 → 좀 더 절제된 표현으로
# ============================================================
for n in nodes:
    if n.get('speaker') == '카스미' and '언니도... 이렇게 어딘가에서 연주하고 있을까요' in n.get('text', ''):
        n['text'] = '...이런 비과학적인 현상을... 언니도 어딘가에서 겪고 있었던 걸까요.'
        print('Fix 5: Kasumi emotional line more measured (node ' + str(n['id']) + ')')

# ============================================================
# Fix 6: 세이카 수첩 → 한계를 인정하면서도 싸우겠다는 의지
# ============================================================
for n in nodes:
    if '이 작은 수첩의 잉크마저 지우진 못할 거야' in n.get('text', ''):
        n['text'] = '시간이 지나면 이 수첩의 잉크마저 지워질지도 몰라. 하지만 지워지기 전에 끊임없이 다시 쓰고, 다시 기억한다면... 현상보다 우리가 한 발 빠를 거야.'
        print('Fix 6: Seika notebook - acknowledges limitation (node ' + str(n['id']) + ')')

reindex(nodes)
data['nodes'] = nodes
save('ch1_resolution.json', data)
print('Saved ch1_resolution.json (' + str(len(nodes)) + ' nodes)')

print('\nAll plausibility fixes applied!')
