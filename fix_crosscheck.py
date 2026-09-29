import json, sys, os

sys.stdout.reconfigure(encoding='utf-8')
base = 'F:/Project-F/Assets/Resources/Data/Dialogues'

# ============================================================
# Fix 1: 5년 주기 나열 시 2021년 포함
# ============================================================
# ch0_origin.json - Node with "2001년, 2006년, 2011년, 2016년"
path = os.path.join(base, 'ch0_origin.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for n in data['nodes']:
    if '2001년, 2006년, 2011년, 2016년' in n.get('text', ''):
        n['text'] = n['text'].replace(
            '2001년, 2006년, 2011년, 2016년. 5년 간격으로 실종자가 발생하는데',
            '2001년, 2006년, 2011년, 2016년, 2021년. 5년 간격으로 실종자가 발생하는데'
        )
        print('Fix 1a: Added 2021 to ch0_origin cycle list (node ' + str(n['id']) + ')')
with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# ch1_resolution.json - Same pattern
path = os.path.join(base, 'ch1_resolution.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for n in data['nodes']:
    if '2001년, 2006년, 2011년, 2016년' in n.get('text', ''):
        n['text'] = n['text'].replace(
            '2001년, 2006년, 2011년, 2016년',
            '2001년, 2006년, 2011년, 2016년, 2021년'
        )
        print('Fix 1b: Added 2021 to ch1_resolution cycle list (node ' + str(n['id']) + ')')

# ============================================================
# Fix 2: 가타카나 → 한글 초성 패턴으로 변경
# ============================================================
for n in data['nodes']:
    if 'ハ... ユ...' in n.get('text', ''):
        n['text'] = "나왔어. 초성 패턴이... 'ㅎ... ㅇ...' 이름이야. 한글로는..."
        print('Fix 2a: Replaced katakana with Korean choseong (node ' + str(n['id']) + ')')
    if "'하... 유...'" in n.get('text', ''):
        n['text'] = "'하... 유...' 나머지는 노이즈에 묻혀서 복원이 안 돼."
        print('Fix 2b: Fixed follow-up line (node ' + str(n['id']) + ')')

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Saved ch1_resolution.json')

# ============================================================
# Fix 3: 에필로그 쿠키 대사 모순 수정
#   resolution에서 모두가 봤으므로, epilogue에서 '몰래' 둔 것처럼 
#   말하면 안 됨
# ============================================================
path = os.path.join(base, 'ch1_epilogue.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

nodes = data['nodes']
for n in nodes:
    if n.get('speaker') == '하루카' and '어젯밤에 피아노 위에 쿠키를' in n.get('text', ''):
        n['text'] = '...아, 저기... 어제 피아노에 두고 온 쿠키... 그분이 드셨을까요?'
        print('Fix 3a: Fixed Haruka cookie line')
    elif n.get('speaker') == '리나' and n.get('text', '') == '뭐? 왜?':
        n['text'] = '당연하지! 안 먹었으면 유령이라도 멱살 잡고 먹였을 테니까.'
        print('Fix 3b: Fixed Rina cookie reaction')
    elif n.get('speaker') == '하루카' and '배고프면 어떡하나' in n.get('text', ''):
        n['text'] = '에헤헤... 그렇겠죠?'
        print('Fix 3c: Fixed Haruka follow-up')
    elif n.get('text', '') == '잠깐의 침묵 후, 리나가 후 하고 웃었다. 카스미도 안경 너머로 살짝 미소를 지었다.':
        n['text'] = '리나가 코끝을 문지르며 웃었다. 카스미도 안경 너머로 살짝 미소를 지었다.'
        print('Fix 3d: Fixed narration')

# Also fix the cookie scene at the end - remove "몰래" since everyone saw it
for n in nodes:
    if '하루카가 몰래 올려두고 간' in n.get('text', ''):
        n['text'] = n['text'].replace('하루카가 몰래 올려두고 간', '하루카가 올려두고 간')
        print('Fix 3e: Removed 몰래 from cookie scene')

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Saved ch1_epilogue.json')

print('\nAll 3 cross-check issues fixed!')
