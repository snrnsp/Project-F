import sys, json
sys.stdout.reconfigure(encoding='utf-8')

# ═══════════ 1. ch1_result_perfect.json 스프라이트 수정 ═══════════
path_perfect = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_result_perfect.json'
with open(path_perfect, 'r', encoding='utf-8-sig') as f:
    raw = f.read()
    while raw.startswith('\ufeff'):
        raw = raw[1:]
    data = json.loads(raw)

fixes_perfect = 0
for node in data['nodes']:
    nid = node['id']
    changed = False
    
    # 세이카/진지 → 세이카/찡그림
    for key in ['characterSpriteLeft', 'characterSpriteCenter', 'characterSpriteRight']:
        if node.get(key) == 'Characters/세이카/진지':
            node[key] = 'Characters/세이카/찡그림'
            print(f"  [perfect] Node {nid}: {key} 세이카/진지 → 세이카/찡그림")
            fixes_perfect += 1
        
        # 세이카/미소 → 세이카/웃음
        if node.get(key) == 'Characters/세이카/미소':
            node[key] = 'Characters/세이카/웃음'
            print(f"  [perfect] Node {nid}: {key} 세이카/미소 → 세이카/웃음")
            fixes_perfect += 1
    
        # 리리스/진지 → 리리스/기본
        if node.get(key) == 'Characters/리리스/진지':
            node[key] = 'Characters/리리스/기본'
            print(f"  [perfect] Node {nid}: {key} 리리스/진지 → 리리스/기본")
            fixes_perfect += 1
    
        # 하루카/슬픔 → 하루카/측은
        if node.get(key) == 'Characters/하루카/슬픔':
            node[key] = 'Characters/하루카/측은'
            print(f"  [perfect] Node {nid}: {key} 하루카/슬픔 → 하루카/측은")
            fixes_perfect += 1

with open(path_perfect, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n✅ ch1_result_perfect.json: {fixes_perfect}건 수정 완료")

# ═══════════ 2. ch1_investigation_talk.json 스프라이트 수정 ═══════════
path_talk = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_investigation_talk.json'
with open(path_talk, 'r', encoding='utf-8-sig') as f:
    raw = f.read()
    while raw.startswith('\ufeff'):
        raw = raw[1:]
    data2 = json.loads(raw)

fixes_talk = 0
for node in data2['nodes']:
    nid = node['id']
    for key in ['characterSpriteLeft', 'characterSpriteCenter', 'characterSpriteRight']:
        if node.get(key) == 'Characters/세이카/미소':
            node[key] = 'Characters/세이카/웃음'
            print(f"  [talk] Node {nid}: {key} 세이카/미소 → 세이카/웃음")
            fixes_talk += 1

with open(path_talk, 'w', encoding='utf-8') as f:
    json.dump(data2, f, ensure_ascii=False, indent=2)

print(f"✅ ch1_investigation_talk.json: {fixes_talk}건 수정 완료")

# ═══════════ 3. 다른 대화 파일에도 미존재 스프라이트가 있는지 전수 조사 ═══════════
import os, glob

valid_sprites = {
    '카스미': ['기본', '경멸', '공포', '당황2', '미소', '시선회피', '찡그림', '측은', '홍조'],
    '리나': ['기본', '경멸', '공포', '놀람', '당황', '웃음', '찡그림', '측은', '홍조'],
    '미나': ['기본', '경멸', '공포', '놀람', '당황', '미소', '삐짐', '음침', '의아', '홍조'],
    '세이카': ['기본', '경멸', '공포', '놀람', '당황', '웃음', '음침', '찡그림', '측은', '홍조'],
    '리리스': ['기본', '경멸', '공포', '놀람', '눈 감음', '미소', '웃음', '음침', '입 벌린 미소', '찡그림', '측은', '홍조'],
    '하루카': ['기본', '경멸', '공포', '놀람', '미소', '삐짐', '웃음', '음침', '측은', '홍조'],
}

dialogues_dir = 'F:/Project-F/Assets/Resources/Data/Dialogues/'
print(f"\n\n═══ 전수 스프라이트 검증 ═══")
issues_found = 0
for filepath in glob.glob(os.path.join(dialogues_dir, '*.json')):
    fname = os.path.basename(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            raw = f.read()
            while raw.startswith('\ufeff'):
                raw = raw[1:]
            fdata = json.loads(raw)
    except:
        continue
    
    for node in fdata.get('nodes', []):
        for key in ['characterSpriteLeft', 'characterSpriteCenter', 'characterSpriteRight']:
            val = node.get(key, '')
            if not val or val.strip() == '':
                continue
            if val.startswith('Characters/'):
                parts = val.split('/')
                if len(parts) >= 3:
                    char_name = parts[1]
                    expression = parts[2]
                    if char_name in valid_sprites:
                        if expression not in valid_sprites[char_name]:
                            print(f"  ❌ {fname} Node {node['id']}: {key} = {val} ('{expression}' 미존재)")
                            issues_found += 1

if issues_found == 0:
    print("  ✅ 모든 스프라이트 참조가 유효합니다!")
else:
    print(f"\n  총 {issues_found}건의 미존재 스프라이트 발견")
