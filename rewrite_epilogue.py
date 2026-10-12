import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

nodes = [
    {"id": 0, "speaker": " ", "text": "다음 날 아침, 네버모어 오컬트 탐정 사무소.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "bg_office_day", "command": "", "noFade": False, "slideIn": False},
    {"id": 1, "speaker": " ", "text": "사무소 식탁에는 일곱 명분의 아침이 차려져 있었다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 2, "speaker": "하루카", "text": "서하유 씨, 단호박 수프 좀 더 드세요! 10년 동안 못 드셨잖아요!", "characterSpriteLeft": "", "characterSpriteCenter": "Characters/하루카/미소", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 3, "speaker": "서하유", "text": "에... 이게 뭔가요? 호박인데... 왜 이렇게 맛있어요...?", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 4, "speaker": "하루카", "text": "그, 그렇죠?! 제 특제 레시피예요!", "characterSpriteLeft": "", "characterSpriteCenter": "Characters/하루카/미소", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 5, "speaker": "리나", "text": "야, 하루카 음식 칭찬하면 끝도 없이 만들어오니까 적당히 해. 호박 라떼, 호박 빙수에 이젠 수프냐!", "characterSpriteLeft": "Characters/리나/찡그림", "characterSpriteCenter": "Characters/하루카/미소", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 6, "speaker": "카스미", "text": "서하유 씨, 가족 연락처를 찾았습니다. 부모님이 아직 노을시에 계시네요.", "characterSpriteLeft": "Characters/카스미/기본", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 7, "speaker": "서하유", "text": "...엄마, 아빠가...? 아직...?", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 8, "speaker": "카스미", "text": "네. 잭오가 데이터를 전 세계에 복원시키면서 사람들의 기억도 함께 돌아왔습니다. 어젯밤 실종 신고가 다시 접수됐더군요.", "characterSpriteLeft": "Characters/카스미/미소", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 9, "speaker": "서하유", "text": "......", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 10, "speaker": " ", "text": "서하유가 식탁 위에 얼굴을 묻고 울기 시작했다. 하루카가 조용히 등을 쓰다듬어 주었다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 11, "speaker": "세이카", "text": "오늘은 가족의 품으로 돌아가. 10년 치 밀린 이야기를 나눠야지.", "characterSpriteLeft": "", "characterSpriteCenter": "Characters/세이카/미소", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 12, "speaker": " ", "text": "— 일주일 후.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "bg_office_day", "command": "", "noFade": False, "slideIn": False},
    {"id": 13, "speaker": " ", "text": "서하유 구출 사건은 전국적인 화제가 되었다. '노을시의 기적'이라 불리며 매스컴을 탔다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 14, "speaker": "리나", "text": "와씨 대박! 소장님, 우리 의뢰가 1,000건이 넘었어!", "characterSpriteLeft": "Characters/리나/웃음", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 15, "speaker": "카스미", "text": "안타깝게도 대부분이 바람난 남편 찾기, 고양이 찾기 같은 일반 의뢰입니다만.", "characterSpriteLeft": "Characters/리나/웃음", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 16, "speaker": "리리스", "text": "서버 과부하 경고. 메일함 용량 99.7%.", "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 17, "speaker": "세이카", "text": "좋아. 이왕 이렇게 된 거, 다 받아주자.", "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/웃음", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 18, "speaker": "미나", "text": "크큭... 이 세상을 어둠에서 구원할 시간인가...", "characterSpriteLeft": "Characters/미나/기본", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/웃음", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 19, "speaker": " ", "text": "그날 저녁, 서하유가 사무소에 다시 찾아왔다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "bg_office_night", "command": "", "noFade": False, "slideIn": False},
    {"id": 20, "speaker": " ", "text": "그리고 거실 한구석에 놓인 낡은 피아노 앞에 앉았다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 21, "speaker": " ", "text": "연주가 시작되었다. 이번에는 슬프고 처연한 곡이 아니었다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 22, "speaker": " ", "text": "10년 동안 혼자 치던 곡이, 누군가가 들어주는 것만으로 전혀 다른 따뜻한 곡이 되었다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 23, "speaker": " ", "text": "연주가 끝나고, 작은 박수가 울렸다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 24, "speaker": "서하유", "text": "...저를 찾아주셔서, 고마워요.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 25, "speaker": " ", "text": "세상에는 아직 과학으로 설명할 수 없는 수많은 미제 사건들이 남아있다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 26, "speaker": " ", "text": "하지만 그들은 더 이상 두렵지 않았다. 잊혀진 이들을 찾아낼, 든든한 동료들이 있으니까.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 27, "speaker": " ", "text": "「네버모어 오컬트 탐정 사무소」의 첫 번째 이야기가, 이렇게 끝났다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 28, "speaker": "", "text": "제작: 사차지\n플레이해주셔서 감사합니다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "bg_black", "command": "", "noFade": False, "slideIn": False},
    {"id": 29, "speaker": " ", "text": "", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "CHANGE_PHASE:Lobby", "noFade": False, "slideIn": False, "nextNodeId": -1}
]

for i in range(len(nodes) - 1):
    nodes[i]['nextNodeId'] = nodes[i+1]['id']
    nodes[i]['choices'] = []
nodes[-1]['choices'] = []

data['nodes'] = nodes

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Rewrote ch1_epilogue ending.")
