import json, sys, os

sys.stdout.reconfigure(encoding='utf-8')
base = 'F:/Project-F/Assets/Resources/Data/Dialogues'

# ============================================================
# Step 1: Trim ch1_result_perfect.json
#   Remove nodes 16-20 (the ending narration, title card, transition)
#   After node 15, transition to ch1_resolution
# ============================================================
path_perfect = os.path.join(base, 'ch1_result_perfect.json')
with open(path_perfect, 'r', encoding='utf-8-sig') as f:
    perfect = json.load(f)

# Keep nodes 0-15, add transition node at 16
new_perfect_nodes = [n for n in perfect['nodes'] if n['id'] <= 15]

# Add transition node
new_perfect_nodes.append({
    "id": 16, "speaker": " ", "text": "",
    "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
    "backgroundSprite": "", "choices": [], "nextNodeId": -1,
    "command": "START_DIALOGUE:ch1_resolution"
})

# Fix nextNodeId chain
for i, n in enumerate(new_perfect_nodes):
    if i < len(new_perfect_nodes) - 1:
        n['nextNodeId'] = i + 1
    else:
        n['nextNodeId'] = -1

perfect['nodes'] = new_perfect_nodes
with open(path_perfect, 'w', encoding='utf-8-sig') as f:
    json.dump(perfect, f, ensure_ascii=False, indent=4)
print('Trimmed ch1_result_perfect.json to ' + str(len(new_perfect_nodes)) + ' nodes')

# ============================================================
# Step 2: Create ch1_resolution.json
# ============================================================
resolution_nodes = [
    # === Act 1: 피아노가 응답한다 ===
    {
        "speaker": " ",
        "text": "세이카의 추리가 끝나자, 음악실 안의 공기가 변했다.",
        "backgroundSprite": "Images/mansion_interior", "command": ""
    },
    {
        "speaker": " ",
        "text": "그리고 다시 — 피아노 건반이 움직이기 시작했다.",
        "backgroundSprite": "", "command": "EFFECT:SHAKE"
    },
    {
        "speaker": "리나",
        "text": "또...?! 또 연주가 시작된 거야?!",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "카스미",
        "text": "기다려요. 이번에는 아까와 다릅니다. 선율이...",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "이번 선율은 아까처럼 처연하고 슬프지 않았다.\n마치 무언가를 '전하려는' 듯, 또박또박 음을 짚어가는 연주였다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "리리스",
        "text": "잭오 음향 센서 가동. 이번 주파수 패턴은... 아까보다 훨씬 복잡해.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "리리스",
        "text": "단순한 멜로디가 아니야. 이건... 반복 구조가 있어. 마치 언어처럼.",
        "backgroundSprite": "", "command": ""
    },

    # === Act 2: 미나의 '시야' ===
    {
        "speaker": "미나",
        "text": ".......",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "미나가 갑자기 눈을 감았다. 양손이 미세하게 떨리고 있었다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "하루카",
        "text": "미, 미나 언니? 괜찮아요?",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "...보여. 누군가가 보여.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "미나의 목소리에서 평소의 중2병 연기는 완전히 사라져 있었다.\n그 자리에는 무언가에 홀린 듯한, 투명한 목소리만 남아 있었다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "젊은 여자야. 스물서넛쯤... 긴 머리카락. 손가락이 길어.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "매일 밤 이 음악실에서 연습하고 있어. 혼자서. 아무도 없는 텅 빈 건물에서.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "콩쿠르... 전국 콩쿠르를 앞두고 있어. 이 사람에게는 피아노밖에 없었어.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "가족도 없고, 친구도 없고... 음악만이 이 사람이 세상에 존재한다는 유일한 증거였어.",
        "backgroundSprite": "", "command": ""
    },

    # === Act 3: 피아니스트의 정체 ===
    {
        "speaker": "카스미",
        "text": "...빛바랜 콩쿠르 프로그램. 참가자 목록에서 이름이 지워진 사람.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "카스미",
        "text": "미나의 증언과 일치합니다. 하지만 이름은... 잉크가 번져서 판독이 불가능합니다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "리리스",
        "text": "잠깐. 지금 연주되고 있는 음파 패턴을 디코딩하면...",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "리리스의 손가락이 노트북 위에서 빠르게 움직였다.\n음파의 반복 구조를 분석하자, 화면에 문자 하나하나가 떠올랐다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "리리스",
        "text": "나왔어. 이름이야. 'ハ... ユ...' 아니, 한글로는...",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "리리스",
        "text": "'하... 유...' 나머지는 노이즈에 묻혀서 복원이 안 돼.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "이름조차 온전히 남기지 못했다는 거야. '잊혀지는 현상'이 그 사람의 이름까지 지우고 있어.",
        "backgroundSprite": "", "command": ""
    },

    # === Act 4: 현상의 정체 ===
    {
        "speaker": "세이카",
        "text": "정리하자. 내가 5년 전부터 추적해온 자료와 종합하면...",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "2001년, 2006년, 2011년, 2016년. 5년 간격으로 노을시 구시가지에서 한 명씩 사라졌어.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "단순한 실종이 아니야. 실종 신고 기록이 사라지고, 주변 사람들의 기억에서도 서서히 지워졌지.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "이 피아니스트는 2016년 주기의 피해자일 가능성이 높아.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "카스미",
        "text": "그렇다면 다음 주기는... 2021년. 그리고 그 다음은 올해, 2026년.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "맞아. 올해 안에 또 한 명이 사라질 수도 있어.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "리나",
        "text": "...그러니까 이 '현상'은 아직 끝나지 않았다는 거잖아. 지금도 누군가를 노리고 있을 수도 있고.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "'현상'은 사람을 죽이는 게 아니야. 존재 자체를 지우는 것이다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "기록이 사라지고, 기억이 사라지고, 이름이 사라지고... 마지막에는 육체마저 투명해져.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "하지만 이 피아니스트는... 아직 완전히 지워지지 않았어.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "음악이 남아 있으니까. 이 건물에 새겨진 음악이, 마지막 실 한 가닥처럼 이 사람을 세상에 붙들어 두고 있는 것이다.",
        "backgroundSprite": "", "command": ""
    },

    # === Act 5: 연결의 순간 ===
    {
        "speaker": "하루카",
        "text": "...그러면 우리가 여기 온 게, 의미가 있었던 건가요?",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "...하루카, 피아노 앞에 가볼래?",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "하루카",
        "text": "네...?! 저, 저요?!",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "그냥 손을 올려놓기만 해도 돼. 괜찮아.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "하루카가 조심스럽게 피아노 앞에 섰다.\n떨리는 손을 천천히 뻗어, 건반 위에 살며시 올려놓았다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": ".......",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "하루카의 손 아래에서, 건반이 따뜻해졌다.",
        "backgroundSprite": "", "command": "EFFECT:FLASH"
    },
    {
        "speaker": "하루카",
        "text": "...따뜻해요. 건반이... 따뜻해요.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "하루카",
        "text": "이 사람이... 여기 있어요. 지금도.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "단 하나의 음이 울렸다.\n하루카가 누른 것이 아니었다. 건반이 스스로 내려갔다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "그 음을 시작으로, 피아노가 다시 연주를 시작했다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "이번 선율은 달랐다.\n처음 들었던 처연한 곡도, 메시지를 전하려던 또박또박한 음도 아니었다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "따뜻하고, 부드럽고, 어딘가 고마운 마음이 담긴 선율이었다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "리나",
        "text": ".......",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "카스미",
        "text": ".......",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "아무도 말하지 않았다. 연주가 끝날 때까지, 여섯 명은 그 자리에 서서 듣고 있었다.",
        "backgroundSprite": "", "command": ""
    },

    # === Act 6: 사건 해결 ===
    {
        "speaker": " ",
        "text": "연주가 끝났다.\n먼지가 천천히 가라앉았다. 창밖에서 첫 번째 새가 울기 시작했다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "...우리가 이 사람을 구할 수는 없어. 아직은.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "하지만 한 가지는 할 수 있지.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "세이카가 수첩을 꺼냈다. 그리고 한 글자 한 글자 또박또박 적기 시작했다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "피아니스트의 흔적. 부서진 건반 위의 손자국. 빛바랜 프로그램에 남은 이름의 조각.\n잭오가 기록한 음파 데이터. 미나가 본 환영. 하루카가 느낀 온기.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "이 사람이 존재했다는 것을 — 우리는 기억한다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "'잊혀지는 현상'은 모든 기록을 지우지. 하지만 우리가 기록을 남기면, 현상과의 싸움이 시작되는 거야.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "카스미",
        "text": "...기억이 곧 저항이라는 뜻입니까.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "그래. 잊혀진 사람을 기억하는 것. 그것이 이 사건에 대한 우리의 답이야.",
        "backgroundSprite": "", "command": ""
    },

    # === Act 7: 새벽, 마무리 ===
    {
        "speaker": " ",
        "text": "새벽의 희미한 빛이 낡은 음악실 창문을 통해 스며들었다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "피아노는 이제 침묵하고 있었다.\n하지만 아까까지의 차갑던 공기가 사라지고, 음악실은 온화한 온기로 가득 차 있었다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "리리스",
        "text": "...잭오의 온도 센서. 피아노 주변 온도가 정상으로 돌아왔어. 아니, 오히려 주변보다 약간 높아.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "...안심한 것이다. 이 사람은.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "미나",
        "text": "누군가 자신을 기억해준다는 것. 잊혀져가는 존재에게 그것은... 아마 이 세상에서 가장 따뜻한 일일 것이다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "리나",
        "text": "...다음에는 반드시 이름까지 찾아내자. '하유' 뭐시기가 아니라, 온전한 이름을.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "그래. 약속하지.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": "세이카",
        "text": "네버모어의 이름에 걸고 맹세한다. 잊혀진 이들을, 반드시 찾아내겠다.",
        "backgroundSprite": "", "command": ""
    },
    {
        "speaker": " ",
        "text": "",
        "backgroundSprite": "", "command": "EFFECT:FLASH"
    },
    {
        "speaker": " ",
        "text": "— 사건 파일1: 잊혀진 피아니스트 — 해결",
        "backgroundSprite": "Images/bg_black", "command": ""
    },
    {
        "speaker": " ",
        "text": "",
        "backgroundSprite": "", "command": "START_DIALOGUE:ch1_epilogue"
    },
]

# Assign IDs and nextNodeId
for i, n in enumerate(resolution_nodes):
    n['id'] = i
    n['nextNodeId'] = i + 1 if i < len(resolution_nodes) - 1 else -1
    if 'characterSpriteLeft' not in n:
        n['characterSpriteLeft'] = ''
    if 'characterSpriteCenter' not in n:
        n['characterSpriteCenter'] = ''
    if 'characterSpriteRight' not in n:
        n['characterSpriteRight'] = ''
    if 'choices' not in n:
        n['choices'] = []

resolution_data = {
    "dialogueId": "ch1_resolution",
    "nodes": resolution_nodes
}

path_resolution = os.path.join(base, 'ch1_resolution.json')
with open(path_resolution, 'w', encoding='utf-8-sig') as f:
    json.dump(resolution_data, f, ensure_ascii=False, indent=4)
print('Created ch1_resolution.json with ' + str(len(resolution_nodes)) + ' nodes')

print('\nDone! Story flow is now:')
print('  ch1_result_perfect -> ch1_resolution -> ch1_epilogue')
