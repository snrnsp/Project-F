import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Keep up to node 99
new_nodes = data['nodes'][:100]

new_end_nodes = [
    {"id": 100, "speaker": "카스미", "text": "이게 대체 뭡니까?! 세상이 다시 서하유 씨를 지우려 하고 있어요! 강력한 이상 자기장입니다!", "characterSpriteLeft": "", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 101, "speaker": "리리스", "text": "잭오, 스펙트럼 풀가동. 서하유 존재 데이터 전 세계 서버로 강제 전송.", "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 102, "speaker": "리리스", "text": "물리적 소멸 방어 프로토콜. 전송률 80%... 90%...", "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 103, "speaker": " ", "text": "잭오가 불꽃을 튀기며 한계에 다달았다. 하지만 리리스는 멈추지 않았다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 104, "speaker": "리나", "text": "조금만 더 버텨! 고철 덩어리야!!", "characterSpriteLeft": "Characters/리나/찡그림", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 105, "speaker": "미나", "text": "영혼의 사슬이여... 그녀의 혼을 현세에 단단히 묶어두어라!", "characterSpriteLeft": "Characters/리나/찡그림", "characterSpriteCenter": "", "characterSpriteRight": "Characters/미나/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 106, "speaker": "하루카", "text": "(투명한 서하유의 손을 꼭 잡으며) 하유 씨! 가지 마세요! 우리랑 같이 가요!", "characterSpriteLeft": "Characters/하루카/미소", "characterSpriteCenter": "", "characterSpriteRight": "Characters/미나/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 107, "speaker": " ", "text": "잭오의 메인보드가 요란한 소리를 내며 전송 완료 100%를 알렸다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 108, "speaker": " ", "text": "그 순간, 거대한 압력이 거짓말처럼 흩어졌다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 109, "speaker": " ", "text": "그리고... 텅 비어 있던 허공에, 온기를 가진 '진짜' 사람의 손이 하루카의 손을 마주 잡았다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 110, "speaker": "서하유", "text": "...따뜻해.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 111, "speaker": " ", "text": "반투명했던 윤곽이 완전히 색을 찾았다. 세상에서 지워졌던 소녀가 10년 만에 온전히 돌아온 것이다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 112, "speaker": "리나", "text": "와씨... 진짜 사람 냄새 나잖아!", "characterSpriteLeft": "Characters/리나/웃음", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 113, "speaker": "카스미", "text": "...물리 법칙을 역행하는 현상을 제 눈으로 볼 줄은 몰랐군요.", "characterSpriteLeft": "Characters/리나/웃음", "characterSpriteCenter": "Characters/카스미/미소", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 114, "speaker": "리리스", "text": "잭오, 임무 완료. 셧다운.", "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteCenter": "Characters/카스미/미소", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 115, "speaker": "세이카", "text": "환영해. 네버모어 오컬트 탐정 사무소에 온 걸.", "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/미소", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 116, "speaker": "서하유", "text": "...감사합니다... 저를, 기억해 주셔서...", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 117, "speaker": " ", "text": "", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "START_DIALOGUE:ch1_epilogue", "noFade": False, "slideIn": False, "nextNodeId": -1}
]

new_nodes.extend(new_end_nodes)
for i in range(len(new_nodes) - 1):
    new_nodes[i]['nextNodeId'] = new_nodes[i+1]['id']

data['nodes'] = new_nodes

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Rewrote ch1_resolution ending.")
