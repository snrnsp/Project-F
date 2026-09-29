import json, sys

sys.stdout.reconfigure(encoding='utf-8')

path = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json'

nodes = [
    # === Part 1: 다음 날 아침, 사무소 ===
    {
        "id": 0, "speaker": " ",
        "text": "다음 날 아침, 네버모어 오컬트 탐정 사무소.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "Images/mansion_interior_morning", "choices": [], "nextNodeId": 1, "command": ""
    },
    {
        "id": 1, "speaker": " ",
        "text": "밤새 조사를 마치고 돌아온 일행은 각자의 방식으로 피로를 달래고 있었다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 2, "command": ""
    },
    {
        "id": 2, "speaker": "하루카",
        "text": "소장님, 단호박 차 드세요. 밤새 조사하시느라 피곤하시죠?",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 3, "command": ""
    },
    {
        "id": 3, "speaker": "세이카",
        "text": "고마워, 하루카. 향이 좋네.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 4, "command": ""
    },
    {
        "id": 4, "speaker": " ",
        "text": "세이카가 찻잔을 감싸 쥐었다. 따뜻한 김이 피어올랐지만, 그녀의 눈은 여전히 먼 곳을 바라보고 있었다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 5, "command": ""
    },

    # === Part 2: 각자의 반응 ===
    {
        "id": 5, "speaker": "리나",
        "text": "아아~ 결국 어제 텅 빈 강당만 뒤지다가 끝났네! 그 피아니스트는 대체 어디로 간 거야?",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 6, "command": ""
    },
    {
        "id": 6, "speaker": "카스미",
        "text": "'어디로'가 아니라 '어디로 지워졌는가'가 맞겠죠. 물리적 실종이 아니니까요.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 7, "command": ""
    },
    {
        "id": 7, "speaker": "카스미",
        "text": "결국 우리는 '잊혀지는 현상'의 흔적만 확인했을 뿐, 현상 자체를 막거나 해결하지는 못했습니다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 8, "command": ""
    },
    {
        "id": 8, "speaker": "리나",
        "text": "......그래도 아무것도 안 한 건 아니잖아. 그 사람이 거기에 있었다는 걸, 적어도 우리는 알게 됐으니까.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 9, "command": ""
    },
    {
        "id": 9, "speaker": " ",
        "text": "평소의 씩씩한 리나답지 않은, 조용한 목소리였다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 10, "command": ""
    },

    # === Part 3: 리리스의 발견 ===
    {
        "id": 10, "speaker": "리리스",
        "text": "잭오의 스캔 데이터는 클라우드에 백업 완료. 다음 징후가 나타나면 바로 추적 가능해.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 11, "command": ""
    },
    {
        "id": 11, "speaker": "리리스",
        "text": "그리고... 한 가지 더.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 12, "command": ""
    },
    {
        "id": 12, "speaker": " ",
        "text": "리리스가 노트북 화면을 돌려 보여주었다. 잭오가 녹음한 음파 데이터의 스펙트로그램이 떠 있었다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 13, "command": ""
    },
    {
        "id": 13, "speaker": "리리스",
        "text": "어젯밤 우리가 떠난 뒤에도 잭오가 계속 녹음하고 있었는데... 새벽 3시 17분에 또 반응이 있었어.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 14, "command": ""
    },
    {
        "id": 14, "speaker": "리리스",
        "text": "이번에는 피아노가 아니야. 새로운 주파수 패턴이야. 디코딩하면...",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 15, "command": ""
    },
    {
        "id": 15, "speaker": "리리스",
        "text": "'...고마워.'",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 16, "command": ""
    },
    {
        "id": 16, "speaker": " ",
        "text": "사무소 안이 잠시 조용해졌다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 17, "command": ""
    },

    # === Part 4: 감정적 반응 ===
    {
        "id": 17, "speaker": "하루카",
        "text": "......그 사람, 우리가 온 걸 알고 있었나봐요.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 18, "command": ""
    },
    {
        "id": 18, "speaker": "리나",
        "text": ".......",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 19, "command": ""
    },
    {
        "id": 19, "speaker": "리나",
        "text": "아 몰라! 나 이런 거 진짜 못 참아!! 다음에는 반드시 직접 만나서 구해줄 거야!",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 20, "command": ""
    },

    # === Part 5: 미나의 경고 ===
    {
        "id": 20, "speaker": "미나",
        "text": "후후... 톱니바퀴는 돌기 시작했다...",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 21, "command": ""
    },
    {
        "id": 21, "speaker": "하루카",
        "text": "미, 미나 언니...?",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 22, "command": ""
    },
    {
        "id": 22, "speaker": "미나",
        "text": "......아, 아니다. 지금 건 평소의 연기가 아니었다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 23, "command": ""
    },
    {
        "id": 23, "speaker": "미나",
        "text": "어젯밤 그 음악실에서... 뭔가 보였어. 단편적인 이미지. 피아노 건반 위로 손가락이 움직이는 것 같은.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 24, "command": ""
    },
    {
        "id": 24, "speaker": "미나",
        "text": "그리고... 그 뒤에 더 큰 뭔가가 있어. 피아니스트 하나로 끝나는 게 아니야.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 25, "command": ""
    },
    {
        "id": 25, "speaker": "카스미",
        "text": "......미나. 지금 그건, 너의 '감'이라는 건가? 아니면 기억 상실 전의 기억인 건가?",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 26, "command": ""
    },
    {
        "id": 26, "speaker": "미나",
        "text": "......몰라. 그걸 내가 알면 좋겠다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 27, "command": ""
    },

    # === Part 6: 카스미의 변화 ===
    {
        "id": 27, "speaker": " ",
        "text": "카스미가 안경을 벗고 눈을 감았다. 한참 동안 무엇인가를 생각하는 듯했다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 28, "command": ""
    },
    {
        "id": 28, "speaker": "카스미",
        "text": "......솔직히 말하겠습니다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 29, "command": ""
    },
    {
        "id": 29, "speaker": "카스미",
        "text": "저는 지금까지 오컬트라는 것을 인정할 수 없었습니다. 과학으로 설명되지 않는 것은 아직 밝혀지지 않은 과학일 뿐이라고 믿어왔습니다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 30, "command": ""
    },
    {
        "id": 30, "speaker": "카스미",
        "text": "하지만 어젯밤 그 피아노 앞에서... 처음으로 과학 너머의 무언가를 느꼈습니다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 31, "command": ""
    },
    {
        "id": 31, "speaker": "카스미",
        "text": "그리고 그것은... 제 언니에게도 일어났을지 모르는 일입니다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 32, "command": ""
    },
    {
        "id": 32, "speaker": " ",
        "text": "카스미가 안경을 다시 쓰며, 평소보다 조금 더 단단한 눈빛으로 말했다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 33, "command": ""
    },
    {
        "id": 33, "speaker": "카스미",
        "text": "......다음 사건도, 끝까지 함께하겠습니다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 34, "command": ""
    },

    # === Part 7: 세이카의 독백과 결의 ===
    {
        "id": 34, "speaker": "세이카",
        "text": "괜찮아. 다음 타겟이 누가 되든, 그 현상이 어디서 일어나든...",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 35, "command": ""
    },
    {
        "id": 35, "speaker": "세이카",
        "text": "우리가 먼저 찾아낼 거야. 잊혀진 피아니스트도, 앞으로 잊혀질 사람들도.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 36, "command": ""
    },
    {
        "id": 36, "speaker": " ",
        "text": "세이카가 자리에서 일어나 창가로 걸어갔다. 아침 햇살이 오래된 유리창을 통해 들어왔다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 37, "command": ""
    },
    {
        "id": 37, "speaker": "세이카",
        "text": "(작은 목소리로) ......아버지가 준 1년. 이제 절반도 안 남았어.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 38, "command": ""
    },
    {
        "id": 38, "speaker": "세이카",
        "text": "하지만 이제는 혼자가 아니잖아.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 39, "command": ""
    },
    {
        "id": 39, "speaker": " ",
        "text": "세이카가 뒤를 돌아보았다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 40, "command": ""
    },
    {
        "id": 40, "speaker": " ",
        "text": "리나가 빙수를 먹으며 리리스에게 장난을 걸고 있었고, 리리스는 무표정하게 노트북을 닫았다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 41, "command": ""
    },
    {
        "id": 41, "speaker": " ",
        "text": "카스미가 보고서를 정리하면서도, 가끔 창밖을 바라보았다. 아마 사라진 언니를 생각하고 있을 것이다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 42, "command": ""
    },
    {
        "id": 42, "speaker": " ",
        "text": "미나가 소파 구석에서 고양이처럼 웅크리고 졸고 있었고, 하루카가 그 위에 담요를 살며시 덮어주었다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 43, "command": ""
    },
    {
        "id": 43, "speaker": "세이카",
        "text": ".......",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 44, "command": ""
    },
    {
        "id": 44, "speaker": "세이카",
        "text": "(미소 지으며) ...좋은 아침이야.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 45, "command": ""
    },

    # === Part 8: 엔딩 내레이션 ===
    {
        "id": 45, "speaker": " ",
        "text": "네버모어 탐정 사무소의 첫 번째 사건은 그렇게 막을 내렸다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 46, "command": ""
    },
    {
        "id": 46, "speaker": " ",
        "text": "사라진 피아니스트를 구하지는 못했다.\n하지만 그곳에 '누군가 있었다'는 것을 증명해냈다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 47, "command": ""
    },
    {
        "id": 47, "speaker": " ",
        "text": "세상이 잊어버린 존재를, 여섯 명의 아웃사이더들만이 기억하고 있다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 48, "command": ""
    },
    {
        "id": 48, "speaker": " ",
        "text": "그리고 그것은 — 5년 주기의 거대한 미스터리를 향한 아주 작은 첫걸음이었다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 49, "command": ""
    },

    # === Part 9: 쿠키 씬 ===
    {
        "id": 49, "speaker": "",
        "text": "",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "Images/bg_black", "choices": [], "nextNodeId": 50, "command": "EFFECT:FLASH"
    },
    {
        "id": 50, "speaker": "",
        "text": "그날 밤.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "Images/city_night", "choices": [], "nextNodeId": 51, "command": ""
    },
    {
        "id": 51, "speaker": "",
        "text": "텅 빈 음악실에서, 다시 한 번 피아노 소리가 울려 퍼졌다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 52, "command": ""
    },
    {
        "id": 52, "speaker": "",
        "text": "이번에는 아무도 듣는 이가 없었다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 53, "command": ""
    },
    {
        "id": 53, "speaker": "",
        "text": "하지만 그 선율은 — 어젯밤과는 달리, 슬프지 않았다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": 54, "command": ""
    },
    {
        "id": 54, "speaker": "",
        "text": "",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "Images/bg_black", "choices": [], "nextNodeId": 55, "command": "EFFECT:FLASH"
    },

    # === Part 10: 크레딧 ===
    {
        "id": 55, "speaker": " ",
        "text": "제작: 사차지\n\n플레이해주셔서 감사합니다.",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "Images/bg_black", "choices": [], "nextNodeId": 56, "command": ""
    },
    {
        "id": 56, "speaker": " ",
        "text": "",
        "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
        "backgroundSprite": "", "choices": [], "nextNodeId": -1, "command": "END"
    }
]

data = {
    "dialogueId": "ch1_epilogue",
    "nodes": nodes
}

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('ch1_epilogue.json updated with ' + str(len(nodes)) + ' nodes')
