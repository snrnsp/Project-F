import sys, json
sys.stdout.reconfigure(encoding='utf-8')

# ═══════════ 1. ch1_night.json — 새 증거 복선 추가 ═══════════
path = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_night.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    raw = f.read()
    while raw.startswith('\ufeff'):
        raw = raw[1:]
    data = json.loads(raw)

nodes = data['nodes']

# Insert foreshadowing nodes:
# After node 13 (먼지 냄새, 바닥에 악보): add footprint hint
# After node 20 (피아노 연주 시작): add temperature hint  

new_nodes = []
for node in nodes:
    new_nodes.append(node)
    
    if node['id'] == 13:
        # Footprint foreshadowing
        new_nodes.append({
            "id": 900,
            "speaker": "리나",
            "text": "어? 바닥에 발자국이 있어. 먼지 위에 선명하게... 어디로 이어지는 거지?",
            "characterSpriteLeft": "Characters/리나/기본",
            "characterSpriteCenter": "",
            "characterSpriteRight": "Characters/카스미/기본",
            "backgroundSprite": "",
            "choices": [],
            "nextNodeId": -1,
            "command": "",
            "noFade": False,
            "slideIn": True
        })

    if node['id'] == 20:
        # Temperature foreshadowing
        new_nodes.append({
            "id": 901,
            "speaker": "하루카",
            "text": "으... 갑자기 엄청 추워졌어요...! 아까까지는 안 이랬는데...!",
            "characterSpriteLeft": "Characters/하루카/공포",
            "characterSpriteCenter": "",
            "characterSpriteRight": "",
            "backgroundSprite": "",
            "choices": [],
            "nextNodeId": -1,
            "command": "",
            "noFade": False,
            "slideIn": True
        })
        new_nodes.append({
            "id": 902,
            "speaker": "리리스",
            "text": "...잭오의 열화상 센서가 이상 반응을 보이고 있어. 피아노 주변 온도가 급격히 하강 중.",
            "characterSpriteLeft": "",
            "characterSpriteCenter": "Characters/리리스/놀람",
            "characterSpriteRight": "",
            "backgroundSprite": "",
            "choices": [],
            "nextNodeId": -1,
            "command": "",
            "noFade": False,
            "slideIn": True
        })

# Renumber
for i, node in enumerate(new_nodes):
    node['id'] = i
    cmd = node.get('command', '')
    if cmd.startswith(('START_DIALOGUE', 'CHANGE_PHASE', 'END')) and cmd:
        node['nextNodeId'] = -1
    elif i + 1 < len(new_nodes):
        node['nextNodeId'] = i + 1
    else:
        node['nextNodeId'] = -1

data['nodes'] = new_nodes
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"✅ ch1_night.json: {len(nodes)} → {len(new_nodes)}노드 (발자국/온도 복선 3노드 추가)")

# ═══════════ 2. ch1_investigation_talk.json — 함정 공개 노드 수정 ═══════════
path2 = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_investigation_talk.json'
with open(path2, 'r', encoding='utf-8-sig') as f:
    raw = f.read()
    while raw.startswith('\ufeff'):
        raw = raw[1:]
    data2 = json.loads(raw)

for node in data2['nodes']:
    if node['id'] == 11:
        # Make the red herring hint ambiguous instead of directly dismissing
        node['text'] = "부서진 메트로놈과 낡은 음악 잡지도 수거했습니다. 모든 증거의 연관성은 아직 단정 지을 수 없으니, 추리 단계에서 신중하게 판단해야 할 것입니다."
        print("  ✅ Node 11: 함정 직접 공개 → 애매한 표현으로 변경")

with open(path2, 'w', encoding='utf-8') as f:
    json.dump(data2, f, ensure_ascii=False, indent=2)
print("✅ ch1_investigation_talk.json 수정 완료")

# ═══════════ 3. ch1_case.json — 유사한 질문 표현 수정 ═══════════
path3 = 'F:/Project-F/Assets/Resources/Data/Cases/ch1_case.json'
with open(path3, 'r', encoding='utf-8-sig') as f:
    raw = f.read()
    while raw.startswith('\ufeff'):
        raw = raw[1:]
    data3 = json.loads(raw)

for q in data3['questions']:
    if q['correctEvidenceId'] == 'dusty_footprints':
        old = q['questionText']
        q['questionText'] = "피아노 주변에서 존재의 이동 흔적을 보여주는 단서는?"
        print(f"  ✅ Q4: '{old}' → '{q['questionText']}'")
    if q['correctEvidenceId'] == 'temperature_anomaly':
        old = q['questionText']
        q['questionText'] = "'현상'이 온도나 기류 등 주변 환경에 미치는 영향의 단서는?"
        print(f"  ✅ Q5: '{old}' → '{q['questionText']}'")

with open(path3, 'w', encoding='utf-8') as f:
    json.dump(data3, f, ensure_ascii=False, indent=2)
print("✅ ch1_case.json 질문 표현 수정 완료")

# ═══════════ 4. ch1_result_fail.json — 점수 기반 피드백 ═══════════
# Note: The fail dialogue is triggered by DeductionManager when NOT perfect.
# We can't dynamically insert score into JSON dialogue, but we CAN make 
# the dialogue feel less generic by referencing "다시 살펴보기"
path4 = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_result_fail.json'

fail_nodes = [
    {"id": 0, "speaker": "카스미", "text": "소장님, 추론의 일부가 맞지 않습니다. 증거와 결론 사이에 논리적 비약이 있어요.",
     "characterSpriteCenter": "Characters/카스미/찡그림",
     "backgroundSprite": "Images/mansion_interior"},
    {"id": 1, "speaker": "카스미", "text": "각 증거가 정확히 무엇을 증명하는지, 하나씩 다시 짚어볼 필요가 있습니다.",
     "characterSpriteCenter": "Characters/카스미/기본"},
    {"id": 2, "speaker": "세이카", "text": "...맞아. 서두르면 안 돼. 증거의 설명을 꼼꼼하게 읽어보자.",
     "characterSpriteLeft": "Characters/세이카/당황", "characterSpriteRight": "Characters/카스미/기본",
     "slideIn": True},
    {"id": 3, "speaker": "리리스", "text": "힌트를 줄게. 증거 중에 이 사건과 직접 관련 없는 것도 섞여 있을 수 있어. 설명을 잘 읽어봐.",
     "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteRight": "Characters/세이카/기본",
     "slideIn": True},
    {"id": 4, "speaker": "미나", "text": "서두르지 마라... 진실은 언제나 증거 속에 숨어 있느니라.",
     "characterSpriteLeft": "Characters/미나/기본", "characterSpriteRight": "Characters/세이카/기본",
     "slideIn": True},
    {"id": 5, "speaker": "", "text": "",
     "command": "CHANGE_PHASE:Deduction"},
]

fail_data = {"dialogueId": "ch1_result_fail", "nodes": []}
for i, n in enumerate(fail_nodes):
    cmd = n.get("command", "")
    if cmd.startswith(("CHANGE_PHASE", "END")):
        next_id = -1
    elif i + 1 < len(fail_nodes):
        next_id = fail_nodes[i + 1]["id"]
    else:
        next_id = -1
    
    fail_data["nodes"].append({
        "id": n["id"],
        "speaker": n.get("speaker", ""),
        "text": n.get("text", ""),
        "characterSpriteLeft": n.get("characterSpriteLeft", ""),
        "characterSpriteCenter": n.get("characterSpriteCenter", ""),
        "characterSpriteRight": n.get("characterSpriteRight", ""),
        "backgroundSprite": n.get("backgroundSprite", ""),
        "choices": [],
        "nextNodeId": next_id,
        "command": cmd,
        "noFade": False,
        "slideIn": n.get("slideIn", False)
    })

with open(path4, 'w', encoding='utf-8') as f:
    json.dump(fail_data, f, ensure_ascii=False, indent=2)
print("✅ ch1_result_fail.json: 재작성 완료 (구체적 피드백 + 힌트 제공)")

print("\n═══ 전체 JSON 수정 완료 ═══")
