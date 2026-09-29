import json, sys, os

sys.stdout.reconfigure(encoding='utf-8')

base = 'F:/Project-F/Assets/Resources/Data/Dialogues'

# ===== 1. ch0_gathering.json =====
path = os.path.join(base, 'ch0_gathering.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for n in data['nodes']:
    if n['id'] == 9:
        n['text'] = '— 2주 후, 리나 합류.'  # fix typo .. -> .
    elif n['id'] == 12:
        n['text'] = '...저 무식한 인간, 놀랍게도 쓸모가 있습니다.'  # remove (보고서)
with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Updated ch0_gathering.json')

# ===== 2. ch0_opening.json =====
path = os.path.join(base, 'ch0_opening.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for n in data['nodes']:
    if n['id'] == 14:
        n['text'] = '...오늘도 여느 때처럼, 저택의 문이 삐걱거리며 열린다.'  # ...... -> ...
with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Updated ch0_opening.json')

# ===== 3. ch1_morning.json =====
path = os.path.join(base, 'ch1_morning.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for n in data['nodes']:
    if n['id'] == 7:
        n['text'] = '...또 호박입니까.'
    elif n['id'] == 17:
        n['text'] = '오 빙수!! 먹을 먹을!! ...잠깐, 왜 또 호박이야?'
    elif n['id'] == 18:
        n['text'] = '...시끄러워.'
    elif n['id'] == 24:
        n['text'] = '상관없어.'
    elif n['id'] == 27:
        n['text'] = '읏?! 야, 언제 온 거야! 놀랬잖아!!'
    elif n['id'] == 38:
        n['text'] = '...폐쇄된 음악실에서 피아노 소리?'
    elif n['id'] == 47:
        n['text'] = '(조용히) ...그 음악실, 예전에 한 피아니스트가 콩쿠르 직전에 갑자기 사라진 곳이다.'
    elif n['id'] == 48:
        n['text'] = '...사라졌다? 실종 사건입니까?'
    elif n['id'] == 49:
        n['text'] = '아니, 더 이상하지. 실종 신고 기록이 없고, 그 피아니스트가 존재했다는 기록 자체가... 거의 없는 것이다.'
    elif n['id'] == 51:
        n['text'] = '...기록이 없다?'
    elif n['id'] == 55:
        n['text'] = '...이건 돈 문제가 아니야.'
    elif n['id'] == 56:
        n['text'] = '(세이카의 표정을 보며) ...알겠습니다. 오늘 밤, 현장 조사를 실시하겠습니다.'
    elif n['id'] == 64:
        n['text'] = '...좋아. 그럼 오늘 밤, 전원 출동이다.'
    elif n['id'] == 68:
        n['text'] = '— 사건 파일1: 잊혀진 피아니스트 —'
with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Updated ch1_morning.json')

# ===== 4. ch1_night.json =====
path = os.path.join(base, 'ch1_night.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for n in data['nodes']:
    if n['id'] == 16:
        n['text'] = '...이 장소에는... 뭔가가 남아있구나. 연기가 아니야, 진짜로.'
    elif n['id'] == 25:
        n['text'] = '잭오 센서는 이상 없어... 이건... 실제로 건반이 눌리고 있는 거야.'
    elif n['id'] == 27:
        n['text'] = '...찾았어. 이 사람이야. 잊혀진 피아니스트.'
with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Updated ch1_night.json')

# ===== 5. ch1_investigation_talk.json =====
path = os.path.join(base, 'ch1_investigation_talk.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for n in data['nodes']:
    if n['id'] == 12:
        n['text'] = '이건... 내가 알고 있는 것과 일치하는구나.'
    elif n['id'] == 13:
        n['text'] = '네? 방금 그 말은...'
    elif n['id'] == 14:
        n['text'] = "'잊혀지는 현상'. 사람의 존재 자체가 세상에서 지워지는 것이다. 기록에서도... 그리고 사람들의 기억 속에서도."
with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Updated ch1_investigation_talk.json')

# ===== 6. ch1_result_perfect.json =====
path = os.path.join(base, 'ch1_result_perfect.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for n in data['nodes']:
    if n['id'] == 8:
        n['text'] = '...과학적으로 말이 안 됩니다. 하지만... 증거가 그렇게 가리키고 있으니 인정할 수밖에 없군요.'
with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Updated ch1_result_perfect.json')

print('\nAll user CSV edits applied to JSON files!')
