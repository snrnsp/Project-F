import sys, json, shutil, os
sys.stdout.reconfigure(encoding='utf-8')

# ═══════════ 백업 ═══════════
for fname in ['ch0_origin.json', 'ch0_gathering.json']:
    src = f'F:/Project-F/Assets/Resources/Data/Dialogues/{fname}'
    bak = f'F:/Project-F/Assets/Resources/Data/Dialogues/_legacy/{fname}.bak'
    if os.path.exists(src):
        os.makedirs(os.path.dirname(bak), exist_ok=True)
        shutil.copy2(src, bak)
        print(f"  백업: {fname} → _legacy/")

# ═══════════ ch0_origin 압축: 51 → 25 노드 ═══════════
origin_nodes = [
    # --- 법원, 5년 전 ---
    {"id": 0, "speaker": "", "text": "— 5년 전. 가을.",
     "backgroundSprite": "Images/bg_flashback"},
    {"id": 1, "speaker": "", "text": "노을시 지방법원. 한 여자가 재판 기록 더미 앞에 앉아 있었다."},
    {"id": 2, "speaker": "세이카", "text": "......이상하다. 노을시 구시가지 실종 사건... 2003년, 2008년, 2014년, 2019년. 5년 간격으로 실종자가 발생하는데, 전부 수사 중단. 기록이 거의 남아있지 않아.",
     "characterSpriteCenter": "Characters/세이카/찡그림", "noFade": True},
    {"id": 3, "speaker": "세이카", "text": "마치 처음부터 존재하지 않았던 사람들처럼.",
     "characterSpriteCenter": "Characters/세이카/찡그림", "noFade": True},
    # --- 상사에게 묵살 ---
    {"id": 4, "speaker": "세이카", "text": "실종 사건 기록에 의도적인 누락이 있는 것 같습니다. 경찰 쪽에서 조직적으로 은폐한 흔적이——",
     "characterSpriteCenter": "Characters/세이카/기본", "noFade": True},
    {"id": 5, "speaker": "", "text": "\"세이카 씨, 우리 로펌의 주요 고객 중에 노을시 경찰청 관계자가 있다는 거 알지? 이 건은 더 이상 건드리지 마.\" 선임은 세이카의 말을 잘랐다."},
    {"id": 6, "speaker": "", "text": "법이 진실을 지켜줄 거라고 믿었다. 하지만 법은 때때로, 진실을 묻는 도구로도 쓰인다."},
    {"id": 7, "speaker": "세이카", "text": "......사라진 사람들. 기록에서 지워진 사람들. 이걸 그냥 넘기면, 나도 공범이 되는 거 아닌가.",
     "characterSpriteCenter": "Characters/세이카/찡그림", "noFade": True},
    # --- 할로윈 밤, 저택 ---
    {"id": 8, "speaker": "", "text": "— 4년 전. 10월 31일. 할로윈 밤.",
     "backgroundSprite": "Images/bg_flashback"},
    {"id": 9, "speaker": "", "text": "실종 사건을 혼자 조사하던 세이카는 모든 사건의 중심에 있는 장소를 찾아냈다. 구시가지 언덕 꼭대기의 '이케다 저택'."},
    {"id": 10, "speaker": "세이카", "text": "할로윈 밤에 유령의 집을 조사하다니...... 영화 같은 전개네.",
     "characterSpriteCenter": "Characters/세이카/기본", "noFade": True},
    {"id": 11, "speaker": "", "text": "삐걱거리는 계단을 올라 3층 서재에 들어선 순간—",
     "command": "EFFECT:SHAKE"},
    {"id": 12, "speaker": "", "text": "아무도 없는 서재에서, 책장의 책들이 한 권씩 스스로 빠져나와 바닥에 쌓이기 시작했다.",
     "command": "EFFECT:FLASH"},
    {"id": 13, "speaker": "세이카", "text": "......뭐야.",
     "characterSpriteCenter": "Characters/세이카/놀람", "noFade": True},
    {"id": 14, "speaker": "", "text": "바닥에 떨어진 책들의 제목을 이으면 하나의 문장이 되었다."},
    {"id": 15, "speaker": "", "text": "「찾아야 한다. 잊혀진 이들을.」",
     "command": "EFFECT:FLASH"},
    {"id": 16, "speaker": "세이카", "text": "......잊혀진 이들. 내가 찾던 답이 여기에 있었던 건가.",
     "characterSpriteCenter": "Characters/세이카/놀람", "noFade": True},
    # --- 결심, 사무소 설립 ---
    {"id": 17, "speaker": "", "text": "경찰에 신고했지만, '기류에 의한 낙하'로 종결. 하지만 세이카에게는 확신이 생겼다."},
    {"id": 18, "speaker": "세이카", "text": "법으로는 안 돼. 경찰도 안 돼. 그렇다면 내가 직접 파헤칠 수밖에 없어.",
     "characterSpriteCenter": "Characters/세이카/기본", "noFade": True},
    {"id": 19, "speaker": "", "text": "로펌 취직을 포기하고, 전 재산과 가족 자금을 투입해 저택을 매입. 1년에 걸친 리모델링 끝에 현관에 새로운 간판이 걸렸다."},
    {"id": 20, "speaker": "", "text": "「네버모어 오컬트 탐정 사무소」",
     "command": "EFFECT:FLASH"},
    {"id": 21, "speaker": "세이카", "text": "할로윈 장식은 반은 내 취향이지만, 나머지 반은 전략이야. '설명할 수 없는 일'을 겪은 사람이 편하게 찾아올 수 있는 분위기를 만들기 위해서.",
     "characterSpriteCenter": "Characters/세이카/웃음", "noFade": True},
    # --- 혼자, 사람이 필요해 ---
    {"id": 22, "speaker": "", "text": "하지만 사무소를 열고 6개월이 지나도록, 의뢰인도 동료도 오지 않았다. 넓은 저택에서 혼자 와인을 마시며 실종자들의 흔적을 추적하는 나날이 이어졌다."},
    {"id": 23, "speaker": "세이카", "text": "혼자서는 한계가 있어. 추리할 사람, 현장을 뛸 사람, 기술을 다룰 사람... 사람이 필요해.",
     "characterSpriteCenter": "Characters/세이카/측은", "noFade": True},
    {"id": 24, "speaker": "", "text": "",
     "command": "START_DIALOGUE:ch0_gathering"},
]

# ═══════════ ch0_gathering 압축: 67 → 38 노드 ═══════════
gathering_nodes = [
    # --- 도입 ---
    {"id": 0, "speaker": "", "text": "부모님이 준 1년의 기한. 이미 6개월이 지났다. 남은 시간은 반 년.",
     "backgroundSprite": "Images/bg_flashback"},
    {"id": 1, "speaker": "", "text": "그런데 구시가지에서 또다시 실종 사건이 발생했다. 5년 주기의 패턴. 다음 실종이 일어날 시기가 바로 올해였다."},
    {"id": 2, "speaker": "세이카", "text": "시작됐어. 더 이상 준비할 시간이 없어.",
     "characterSpriteCenter": "Characters/세이카/찡그림", "noFade": True},
    {"id": 3, "speaker": "", "text": "실종 사건의 파장 속에서, 각자의 이유로 진실에 가까이 있던 사람들이 움직이기 시작했다."},
    # --- 카스미 ---
    {"id": 4, "speaker": "", "text": "— 카스미 합류. 실종 발생 직후."},
    {"id": 5, "speaker": "", "text": "경찰청 과학수사대 인턴. 어린 시절 사라진 언니를 찾기 위해 수사의 길을 택했지만, '설명할 수 없는 현장'을 무조건 덮는 관행에 지쳐 있었다."},
    {"id": 6, "speaker": "세이카", "text": "한 장의 사진을 보여줄게. 네 언니가 실종된 현장에서 발견된 건데...... 경찰 보고서에는 없는 증거물이야.",
     "characterSpriteLeft": "Characters/세이카/기본", "noFade": True},
    {"id": 7, "speaker": "카스미", "text": "...이걸 어디서 구하셨습니까.",
     "characterSpriteLeft": "Characters/세이카/기본", "characterSpriteRight": "Characters/카스미/기본", "noFade": True},
    {"id": 8, "speaker": "카스미", "text": "......좋습니다. 다만 한 가지. 유령 운운하는 소리는 하지 마십시오.",
     "characterSpriteLeft": "Characters/세이카/웃음", "characterSpriteRight": "Characters/카스미/기본", "noFade": True},
    # --- 리나 ---
    {"id": 9, "speaker": "", "text": "— 리나 합류. 카스미 합류 2주 후."},
    {"id": 10, "speaker": "", "text": "첫 번째 의뢰 현장에서, 실종된 후배를 찾으러 혼자 뛰어든 여자와 마주쳤다."},
    {"id": 11, "speaker": "리나", "text": "경찰이 안 움직이면 내가 직접 찾으면 되잖아! 뭘 그렇게 쳐다봐?!",
     "characterSpriteCenter": "Characters/리나/기본", "slideIn": True, "slideFromRight": True, "noFade": True},
    {"id": 12, "speaker": "카스미", "text": "(보고서) ......저 무식한 사람, 놀랍게도 쓸모가 있습니다.",
     "characterSpriteLeft": "Characters/카스미/찡그림", "characterSpriteCenter": "Characters/리나/기본", "characterSpriteRight": "Characters/세이카/웃음", "noFade": True},
    {"id": 13, "speaker": "리나", "text": "어차피 딱히 하는 것도 없었고, 여기 일이 재밌잖아. 그리고 밥도 주고.",
     "characterSpriteLeft": "Characters/카스미/찡그림", "characterSpriteCenter": "Characters/리나/웃음", "characterSpriteRight": "Characters/세이카/웃음", "noFade": True},
    # --- 리리스 ---
    {"id": 14, "speaker": "", "text": "— 리리스 합류. 리나 합류 1달 후.",
     "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteRight": "Characters/세이카/기본"},
    {"id": 15, "speaker": "", "text": "온라인에서 「유령 드론(GhostDrone)」이라는 이름으로 활동하던 프리랜서 해커. 자작 드론으로 구시가지를 촬영하다가, 30년간 비어있는 폐건물에서 있을 수 없는 열원을 포착했다.",
     "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteRight": "Characters/세이카/기본"},
    {"id": 16, "speaker": "세이카", "text": "그 드론 영상, 결정적인 증거였어. 우리랑 같이 일할 생각 없어?",
     "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteRight": "Characters/세이카/기본", "noFade": True},
    {"id": 17, "speaker": "리리스", "text": "...작업실이 필요했는데. 여기 3층 빈 방 쓸 수 있어?",
     "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteRight": "Characters/세이카/기본", "noFade": True},
    {"id": 18, "speaker": "", "text": "이후 3층 다락방을 자신의 작업실로 개조하여 입주. 정찰 드론 「잭오(Jack-O)」가 만들어진 것도 이 시기였다."},
    # --- 미나 ---
    {"id": 19, "speaker": "", "text": "— 미나 합류. 리리스 합류 2주 후."},
    {"id": 20, "speaker": "", "text": "가장 미스터리한 합류. 어느 비 오는 밤, 저택 현관 앞에 쓰러져 있는 채로 발견되었다. 신원 불명. 이름이 '미나'라는 것 외에는 아무것도 기억나지 않는다고 주장했다."},
    {"id": 21, "speaker": "미나", "text": "크큭... 미나라고 하느니라. 천 년을 묵은 원혼이 인간의 몸을 빌려 이곳에 나타난 것이다......",
     "characterSpriteCenter": "Characters/미나/기본", "noFade": True},
    {"id": 22, "speaker": "카스미", "text": "......기억상실 환자의 망상으로 보입니다.",
     "characterSpriteLeft": "Characters/카스미/찡그림", "characterSpriteRight": "Characters/미나/기본", "noFade": True},
    {"id": 23, "speaker": "", "text": "하지만 미나에게는 설명할 수 없는 능력이 있었다. 한 번도 가보지 않은 폐건물의 구조를 알고, 사건의 결말을 예언하듯 중얼거리면, 그것이 맞았다."},
    {"id": 24, "speaker": "세이카", "text": "미나는... 이 저택이 부른 거야. 아마.",
     "characterSpriteCenter": "Characters/세이카/기본", "noFade": True},
    # --- 하루카 ---
    {"id": 25, "speaker": "", "text": "— 하루카 합류. 미나 합류 약 3주 후."},
    {"id": 26, "speaker": "", "text": "구시가지의 작은 카페에서 아르바이트를 하던 19세 소녀. 학교에서 심한 따돌림을 당해 자퇴한 뒤, 혼자서 생계를 유지하고 있었다."},
    {"id": 27, "speaker": "리나", "text": "넌 사람을 잘 보는 눈이 있네. 우리 사무소에 올래? 밥도 나오고 방도 줄 수 있어.",
     "characterSpriteCenter": "Characters/리나/기본", "noFade": True},
    {"id": 28, "speaker": "하루카", "text": "여기... 진짜 무섭긴 한데... 되게 따뜻해요.",
     "characterSpriteCenter": "Characters/하루카/홍조", "noFade": True},
    {"id": 29, "speaker": "", "text": "하루카가 오고 나서 저택에는 항상 호박으로 만든 무언가의 냄새가 풍기게 되었다."},
    # --- 총정리 ---
    {"id": 30, "speaker": "", "text": "불과 3개월 남짓한 시간 동안, 다섯 명이 연달아 합류했다. 실종 사건이라는 파장이 각자의 삶에 금을 내면서, 갈 곳 없는 사람들이 같은 장소로 흘러들어온 것이다."},
    {"id": 31, "speaker": "세이카", "text": "......그러고 보니, 전부 여자네. 일부러 그런 건 아니야. 그냥 결과적으로 이렇게 된 거지.",
     "characterSpriteCenter": "Characters/세이카/웃음", "noFade": True},
    {"id": 32, "speaker": "세이카", "text": "시스템 밖으로 밀려난 사람들. 기존 질서에서 제 자리를 찾지 못한 사람들. 그런 사람들이 이 으스스한 저택에 모인 거야.",
     "characterSpriteCenter": "Characters/세이카/기본", "noFade": True},
    {"id": 33, "speaker": "세이카", "text": "어쩌면 이 저택이 부른 건지도 몰라. '잊혀진 이들'을 찾으려면, 세상에서 한번쯤 잊혀본 사람이어야 하니까.",
     "characterSpriteCenter": "Characters/세이카/기본", "noFade": True},
    {"id": 34, "speaker": "", "text": "부모님이 준 1년의 기한. 그 마감 직전에 기적처럼 팀이 갖춰졌다. 경찰이 닫아버린 파일을 다시 여는 사람들. 세상이 외면한 것들을 마주하는 사람들."},
    {"id": 35, "speaker": "", "text": "그리고 지금—"},
    {"id": 36, "speaker": "", "text": "",
     "command": "START_DIALOGUE:ch0_opening"},
]


def build_node(n, next_id):
    """Build a complete node dict with all required fields."""
    node = {
        "id": n["id"],
        "speaker": n.get("speaker", ""),
        "text": n.get("text", ""),
        "characterSpriteLeft": n.get("characterSpriteLeft", ""),
        "characterSpriteCenter": n.get("characterSpriteCenter", ""),
        "characterSpriteRight": n.get("characterSpriteRight", ""),
        "backgroundSprite": n.get("backgroundSprite", ""),
        "choices": n.get("choices", []),
        "nextNodeId": next_id,
        "command": n.get("command", ""),
    }
    if n.get("noFade"):
        node["noFade"] = True
    if n.get("slideIn"):
        node["slideIn"] = True
    if n.get("slideFromRight"):
        node["slideFromRight"] = True
    return node


def build_dialogue(dialogue_id, raw_nodes):
    nodes = []
    for i, n in enumerate(raw_nodes):
        if n.get("command", "").startswith("START_DIALOGUE") or n.get("command") == "END":
            next_id = -1
        elif i + 1 < len(raw_nodes):
            next_id = raw_nodes[i + 1]["id"]
        else:
            next_id = -1
        nodes.append(build_node(n, next_id))
    return {"dialogueId": dialogue_id, "nodes": nodes}


# Write ch0_origin
origin_data = build_dialogue("ch0_origin", origin_nodes)
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json', 'w', encoding='utf-8') as f:
    json.dump(origin_data, f, ensure_ascii=False, indent=2)
print(f"\n✅ ch0_origin.json: 51 → {len(origin_nodes)}노드로 압축 완료")

# Write ch0_gathering
gathering_data = build_dialogue("ch0_gathering", gathering_nodes)
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'w', encoding='utf-8') as f:
    json.dump(gathering_data, f, ensure_ascii=False, indent=2)
print(f"✅ ch0_gathering.json: 67 → {len(gathering_nodes)}노드로 압축 완료")

total_before = 51 + 67
total_after = len(origin_nodes) + len(gathering_nodes)
saved = total_before - total_after
print(f"\n📊 프롤로그 총 노드: {total_before} → {total_after} ({saved}노드 절약, 약 {saved * 6 // 60}분 단축)")
