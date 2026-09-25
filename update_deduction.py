import sys, json
sys.stdout.reconfigure(encoding='utf-8')

# ═══════════ 1. ch1_evidence.json — 3개 → 7개 (핵심 5 + 함정 2) ═══════════
evidence_data = {
    "evidences": [
        # ── 핵심 증거 5개 (required: true) ──
        {
            "id": "dustless_keys",
            "evidenceName": "먼지 없는 건반",
            "description": "폐쇄된 지 수년이 지난 건물인데, 피아노 건반 위에만 먼지가 없다. 누군가, 혹은 무언가가 최근까지 이 피아노를 연주했다는 물리적 증거.",
            "iconPath": "",
            "required": True
        },
        {
            "id": "faded_program",
            "evidenceName": "빛바랜 콩쿠르 프로그램",
            "description": "보면대 위에서 발견된 낡은 콩쿠르 프로그램. 출연자 명단에 한 사람의 이름만 잉크가 번져 거의 읽을 수 없다. 시간에 의한 훼손이 아닌, 존재 자체가 지워지는 것 같은 비정상적인 소실.",
            "iconPath": "",
            "required": True
        },
        {
            "id": "sound_analysis",
            "evidenceName": "음파 분석 데이터",
            "description": "잭오 드론이 기록한 피아노 음파. 건반 주파수와 일치하지만, 일반 피아노에서는 절대 나올 수 없는 이상 주파수 대역이 섞여 있다. 디코딩하면 일정한 패턴이 반복된다.",
            "iconPath": "",
            "required": True
        },
        {
            "id": "dusty_footprints",
            "evidenceName": "사라지는 발자국",
            "description": "음악실 바닥의 먼지 위에 피아노를 향해 걸어간 발자국이 찍혀 있다. 그런데 피아노에서 약 2미터 전에서 발자국이 갑자기 끊긴다. 마치 걸어가던 존재가 중간에 사라진 것처럼.",
            "iconPath": "",
            "required": True
        },
        {
            "id": "temperature_anomaly",
            "evidenceName": "국소 온도 하강 기록",
            "description": "잭오의 열화상 센서가 기록한 데이터. 피아노 연주가 시작되자 피아노 반경 1미터 내의 기온만 5.3도 급격히 하강했다. 연주가 끝나자 정상 온도로 복구. 자연현상으로는 설명 불가능.",
            "iconPath": "",
            "required": True
        },
        # ── 함정 증거 2개 (required: false) ──
        {
            "id": "broken_metronome",
            "evidenceName": "부서진 메트로놈",
            "description": "피아노 옆 선반에서 발견된 기계식 메트로놈. 태엽이 끊어져 작동하지 않는다. 제조 연도는 1980년대. 오랜 세월에 의한 일반적인 노후화로 보인다.",
            "iconPath": "",
            "required": False
        },
        {
            "id": "old_music_magazine",
            "evidenceName": "낡은 음악 잡지",
            "description": "선반 뒤편에서 발견된 1990년대 음악 전문 잡지. 이 건물이 과거에 음악 학원으로 사용되었음을 보여준다. 특정 인물에 대한 기사는 포함되어 있지 않다.",
            "iconPath": "",
            "required": False
        }
    ]
}

with open('F:/Project-F/Assets/Resources/Data/Evidence/ch1_evidence.json', 'w', encoding='utf-8') as f:
    json.dump(evidence_data, f, ensure_ascii=False, indent=2)
print("✅ ch1_evidence.json: 3개 → 7개 (핵심 5 + 함정 2)")

# ═══════════ 2. ch1_case.json — 3문제 → 5문제 ═══════════
case_data = {
    "caseId": "ch1_case",
    "caseName": "잊혀진 피아니스트",
    "questions": [
        {
            "questionText": "누군가가 최근까지 이 피아노를 연주했다는 물리적 증거는?",
            "correctEvidenceId": "dustless_keys"
        },
        {
            "questionText": "피아니스트가 이 음악실에 존재했다는 유일한 기록은?",
            "correctEvidenceId": "faded_program"
        },
        {
            "questionText": "연주된 소리가 일반적인 피아노 음향이 아니라는 결정적 단서는?",
            "correctEvidenceId": "sound_analysis"
        },
        {
            "questionText": "보이지 않는 존재가 이 공간을 물리적으로 이동했다는 증거는?",
            "correctEvidenceId": "dusty_footprints"
        },
        {
            "questionText": "'현상'이 주변 환경에 미치는 비정상적 물리 영향의 증거는?",
            "correctEvidenceId": "temperature_anomaly"
        }
    ],
    "perfectDialogueId": "ch1_result_perfect",
    "failDialogueId": "ch1_result_fail"
}

with open('F:/Project-F/Assets/Resources/Data/Cases/ch1_case.json', 'w', encoding='utf-8') as f:
    json.dump(case_data, f, ensure_ascii=False, indent=2)
print("✅ ch1_case.json: 3문제 → 5문제")

# ═══════════ 3. ch1_investigation_talk.json — 새 증거 반영하여 재작성 ═══════════
talk_nodes = [
    # --- 도입 ---
    {"id": 0, "speaker": "리나", "text": "수색은 이쯤 하면 된 것 같은데! 카스미, 단서들 좀 정리해줄래?",
     "characterSpriteLeft": "Characters/리나/기본", "characterSpriteRight": "Characters/카스미/기본",
     "backgroundSprite": "Images/mansion_interior", "slideIn": True},
    {"id": 1, "speaker": "카스미", "text": "...네. 수집된 단서를 바탕으로 현재 상황을 종합해보겠습니다.",
     "characterSpriteLeft": "Characters/리나/기본", "characterSpriteRight": "Characters/카스미/기본"},

    # --- 먼지 없는 건반 ---
    {"id": 2, "speaker": "카스미", "text": "첫 번째, '먼지 없는 건반'. 건반에는 물리적인 압력이 가해진 흔적이 있지만, 기계 장치 같은 건 전혀 발견되지 않았습니다.",
     "characterSpriteCenter": "Characters/카스미/기본"},
    {"id": 3, "speaker": "카스미", "text": "즉, 눈에 보이지 않는 무언가가 피아노를 쳤다는 결론밖에 나오지 않습니다.",
     "characterSpriteCenter": "Characters/카스미/찡그림"},

    # --- 사라지는 발자국 (NEW) ---
    {"id": 4, "speaker": "리나", "text": "그리고 바닥에 발자국도 있었잖아! 피아노 쪽으로 걸어가다가 도중에 뚝 끊기는 거.",
     "characterSpriteLeft": "Characters/리나/기본", "characterSpriteRight": "Characters/카스미/찡그림", "slideIn": True},
    {"id": 5, "speaker": "카스미", "text": "맞습니다. 먼지 위에 선명한 발자국이 피아노를 향하고 있었는데, 약 2미터 전에서 갑자기 사라졌습니다. 걸어가던 존재가 중간에 소멸한 것처럼.",
     "characterSpriteLeft": "Characters/리나/기본", "characterSpriteRight": "Characters/카스미/찡그림"},

    # --- 음파 분석 + 온도 이상 ---
    {"id": 6, "speaker": "리리스", "text": "잭오의 데이터도 이상해. '음파 분석 데이터'에 따르면 피아노 주파수에 물리 법칙을 무시하는 비정상 대역이 섞여 있어.",
     "characterSpriteLeft": "Characters/카스미/찡그림", "characterSpriteRight": "Characters/리리스/기본", "slideIn": True},
    {"id": 7, "speaker": "리리스", "text": "그리고 하나 더. 연주가 시작되자 피아노 주변 온도만 5도 이상 급격히 떨어졌어. 연주가 끝나니까 바로 원래대로 돌아왔고.",
     "characterSpriteLeft": "Characters/카스미/찡그림", "characterSpriteRight": "Characters/리리스/기본"},
    {"id": 8, "speaker": "카스미", "text": "국소적 온도 하강이라... 말도 안 됩니다. 아무리 그래도... 아니, 교차 검증된 데이터를 부정할 수는 없겠군요.",
     "characterSpriteLeft": "Characters/카스미/찡그림", "characterSpriteRight": "Characters/리리스/기본"},

    # --- 콩쿠르 프로그램 ---
    {"id": 9, "speaker": "하루카", "text": "저, 저기... 악보대에 있던 '빛바랜 콩쿠르 프로그램'은요...? 한 사람의 이름만 지워져 있었어요...",
     "characterSpriteLeft": "Characters/카스미/기본", "characterSpriteRight": "Characters/하루카/공포", "slideIn": True},
    {"id": 10, "speaker": "카스미", "text": "그렇습니다. 잉크가 번진 흔적을 보면 단순한 시간의 흐름에 의한 훼손이 아닙니다. 누군가 고의로... 혹은 알 수 없는 현상에 의해 그 사람의 존재 자체가 지워진 것처럼 보입니다.",
     "characterSpriteLeft": "Characters/카스미/찡그림", "characterSpriteRight": "Characters/하루카/공포"},

    # --- 함정 증거 정리 (NEW) ---
    {"id": 11, "speaker": "카스미", "text": "참고로 부서진 메트로놈과 낡은 음악 잡지도 수거했지만, 이것들은 건물의 용도를 보여줄 뿐 사건과 직접적인 연관은 없어 보입니다.",
     "characterSpriteCenter": "Characters/카스미/기본"},

    # --- 미나 진지 모드 ---
    {"id": 12, "speaker": "미나", "text": "이건... 내가 알고 있는 것과 일치해.",
     "characterSpriteLeft": "Characters/미나/음침", "characterSpriteRight": "Characters/카스미/찡그림", "slideIn": True},
    {"id": 13, "speaker": "카스미", "text": "네? 방금 그 말투는...",
     "characterSpriteLeft": "Characters/미나/음침", "characterSpriteRight": "Characters/카스미/찡그림"},
    {"id": 14, "speaker": "미나", "text": "'잊혀지는 현상'. 사람의 존재 자체가 세상에서 지워지는 거야. 기록에서도... 그리고 사람들의 기억 속에서도.",
     "characterSpriteLeft": "Characters/미나/기본", "characterSpriteRight": "Characters/카스미/찡그림"},
    {"id": 15, "speaker": "카스미", "text": "존재 자체가 지워진다고요? 증명할 수 없는 너무 비약적인 가설입니다.",
     "characterSpriteLeft": "Characters/미나/기본", "characterSpriteRight": "Characters/카스미/찡그림"},

    # --- 세이카 연결 ---
    {"id": 16, "speaker": "세이카", "text": "아니, 카스미. 미나의 말이 맞을지도 몰라.",
     "characterSpriteLeft": "Characters/세이카/기본", "characterSpriteRight": "Characters/카스미/찡그림", "slideIn": True},
    {"id": 17, "speaker": "세이카", "text": "내가 예전에 조사했던 자료 중에, 5년 주기로 발생하는 기묘한 실종 사건 패턴이 있었거든.",
     "characterSpriteLeft": "Characters/세이카/기본", "characterSpriteRight": "Characters/카스미/기본"},
    {"id": 18, "speaker": "세이카", "text": "단순한 실종이 아니었어. 그 사람에 대한 모든 기록이 사라지고, 심지어 가족들의 기억조차 서서히 지워지는 기괴한 현상이었지.",
     "characterSpriteLeft": "Characters/세이카/음침", "characterSpriteRight": "Characters/카스미/기본"},
    {"id": 19, "speaker": "세이카", "text": "이제 퍼즐 조각을 맞춰보자. 다섯 가지 단서가 무엇을 의미하는지.",
     "characterSpriteLeft": "Characters/세이카/웃음", "characterSpriteRight": "Characters/카스미/기본"},

    # --- 종료 ---
    {"id": 20, "speaker": "", "text": "",
     "command": "CHANGE_PHASE:Deduction"},
]

talk_data = {"dialogueId": "ch1_investigation_talk", "nodes": []}
for i, n in enumerate(talk_nodes):
    if n.get("command", "").startswith("CHANGE_PHASE") or n.get("command") == "END":
        next_id = -1
    elif i + 1 < len(talk_nodes):
        next_id = talk_nodes[i + 1]["id"]
    else:
        next_id = -1
    
    node = {
        "id": n["id"],
        "speaker": n.get("speaker", ""),
        "text": n.get("text", ""),
        "characterSpriteLeft": n.get("characterSpriteLeft", ""),
        "characterSpriteCenter": n.get("characterSpriteCenter", ""),
        "characterSpriteRight": n.get("characterSpriteRight", ""),
        "backgroundSprite": n.get("backgroundSprite", ""),
        "choices": [],
        "nextNodeId": next_id,
        "command": n.get("command", ""),
        "noFade": False,
        "slideIn": n.get("slideIn", False)
    }
    talk_data["nodes"].append(node)

with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch1_investigation_talk.json', 'w', encoding='utf-8') as f:
    json.dump(talk_data, f, ensure_ascii=False, indent=2)
print(f"✅ ch1_investigation_talk.json: 18노드 → {len(talk_nodes)}노드 (새 증거 반영)")

# ═══════════ 요약 ═══════════
print(f"""
═══════════════════════════════════════
📊 추리 난이도 변경 요약
═══════════════════════════════════════
증거: 3개 → 7개 (핵심 5 + 함정 2)
질문: 3개 → 5개
경우의 수: 3!=6 → 7×6×5×4×3=2,520 (420배 증가)
함정 제거 후에도: 5!=120 (20배 증가)

핵심 증거:
  1. 먼지 없는 건반 (기존)
  2. 빛바랜 콩쿠르 프로그램 (기존)
  3. 음파 분석 데이터 (기존)
  4. 사라지는 발자국 (NEW)
  5. 국소 온도 하강 기록 (NEW)

함정 증거 (채집 가능하지만 정답 아님):
  6. 부서진 메트로놈 (NEW)
  7. 낡은 음악 잡지 (NEW)
═══════════════════════════════════════
""")
