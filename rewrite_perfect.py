import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_result_perfect.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

nodes = [
    {"id": 0, "speaker": " ", "text": "세이카가 수집된 단서들을 화이트보드 위에 펼쳐 놓듯 늘어놓았다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 1, "speaker": "세이카", "text": "정리해 보자. 처음엔 누군가의 지독한 장난이거나, 흔한 유령 소동이라고 생각했어.", "characterSpriteLeft": "", "characterSpriteCenter": "Characters/세이카/기본", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 2, "speaker": "세이카", "text": "하지만 단서들이 가리키는 건 하나야. 물리적인 죽음이 아니라... '존재의 소멸'.", "characterSpriteLeft": "", "characterSpriteCenter": "Characters/세이카/기본", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 3, "speaker": "카스미", "text": "...그게 과학적으로 성립할 수 있다고 보십니까? 질량 보존의 법칙을 정면으로 위배하는 일입니다.", "characterSpriteLeft": "Characters/카스미/기본", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 4, "speaker": "리나", "text": "아 쫌! 과학 타령 좀 그만해! 네 눈으로 직접 발자국 끊기는 거 봤잖아!", "characterSpriteLeft": "Characters/카스미/기본", "characterSpriteCenter": "Characters/리나/찡그림", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 5, "speaker": "카스미", "text": "그래서 미치겠다는 겁니다! 관측된 데이터와 물리 법칙이 충돌하고 있으니까요!", "characterSpriteLeft": "Characters/카스미/기본", "characterSpriteCenter": "Characters/리나/찡그림", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 6, "speaker": "하루카", "text": "그럼... 이 사람은 지금 어떻게 되어가고 있는 건가요...?", "characterSpriteLeft": "Characters/하루카/미소", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 7, "speaker": "세이카", "text": "기억에서 잊혀지고, 기록에서 지워지고, 결국에는 물리적인 형태마저 증발해 버리는 중이겠지.", "characterSpriteLeft": "Characters/하루카/미소", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 8, "speaker": "세이카", "text": "발자국이 중간에 끊긴 건 증거를 인멸한 게 아니야.", "characterSpriteLeft": "Characters/하루카/미소", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 9, "speaker": "세이카", "text": "피아노를 치러 걸어가던 '도중'에, 발자국을 남길 수 있는 물리적인 육체 자체가 통째로 사라져 버린 거지.", "characterSpriteLeft": "Characters/하루카/미소", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 10, "speaker": "리나", "text": "......미쳤네, 진짜.", "characterSpriteLeft": "Characters/리나/기본", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 11, "speaker": "카스미", "text": "그렇다면 '먼지 없는 건반'과 '영하의 온도'는 어떻게 설명할 겁니까? 육체가 없다면 물리적인 압력을 가할 수 없어요.", "characterSpriteLeft": "Characters/리나/기본", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 12, "speaker": "미나", "text": "육체가 아니라... 집념이니라.", "characterSpriteLeft": "Characters/미나/기본", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 13, "speaker": "카스미", "text": "미나 씨?", "characterSpriteLeft": "Characters/미나/기본", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 14, "speaker": "미나", "text": "인간이 세상을 떠날 때 가장 두려워하는 것이 무엇인 줄 아느냐.", "characterSpriteLeft": "Characters/미나/기본", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 15, "speaker": "미나", "text": "죽음? 아니... '아무도 나를 기억해주지 않는다'는 공포다.", "characterSpriteLeft": "Characters/미나/기본", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 16, "speaker": "세이카", "text": "맞아. 잭오의 주파수 분석 결과를 봐.", "characterSpriteLeft": "Characters/미나/기본", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 17, "speaker": "세이카", "text": "그건 원혼이 깃든 무서운 소리가 아니었어.", "characterSpriteLeft": "Characters/미나/기본", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 18, "speaker": "세이카", "text": "육체가 부서져 나가는 그 순간에도, 오직 자기를 기억해 달라고... 나 여기 있다고...", "characterSpriteLeft": "Characters/미나/기본", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 19, "speaker": "세이카", "text": "필사적으로 허공의 건반을 두드리는, 한 인간의 가장 처절한 절규야.", "characterSpriteLeft": "Characters/미나/기본", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 20, "speaker": "하루카", "text": "아아... 흑...", "characterSpriteLeft": "Characters/하루카/미소", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 21, "speaker": " ", "text": "하루카가 두 손으로 입을 틀어막고 주저앉았다.", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": False},
    {"id": 22, "speaker": "리리스", "text": "데이터 재분석... 확률 99.9%. 피아니스트는 현재 육체를 상실했으나, 의식은 이 공간에 잔존.", "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 23, "speaker": "카스미", "text": "...인정하겠습니다. 과학의 패배를. 그리고...", "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 24, "speaker": "카스미", "text": "...이 잔혹한 현상을 멈춰야 한다는 것도요.", "characterSpriteLeft": "Characters/리리스/기본", "characterSpriteCenter": "Characters/카스미/기본", "characterSpriteRight": "", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 25, "speaker": "리나", "text": "그래서 소장님! 우리 이제 어떻게 하면 되는데! 확 다 때려 부수면 돼?!", "characterSpriteLeft": "Characters/리나/찡그림", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": False, "slideIn": True},
    {"id": 26, "speaker": "세이카", "text": "때려 부수는 건 안 돼. 이번 사건의 적은 물리적인 괴물이 아니니까.", "characterSpriteLeft": "Characters/리나/찡그림", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/미소", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 27, "speaker": "세이카", "text": "우리가 싸워야 할 대상은 '망각(Oblivion)'이야.", "characterSpriteLeft": "Characters/리나/찡그림", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/기본", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 28, "speaker": "세이카", "text": "가자. 저 피아니스트의 이름을 되찾아주러.", "characterSpriteLeft": "Characters/리나/찡그림", "characterSpriteCenter": "", "characterSpriteRight": "Characters/세이카/미소", "backgroundSprite": "", "command": "", "noFade": True, "slideIn": False},
    {"id": 29, "speaker": " ", "text": "", "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "", "backgroundSprite": "", "command": "START_DIALOGUE:ch1_resolution", "noFade": False, "slideIn": False, "nextNodeId": -1}
]

for i in range(len(nodes) - 1):
    nodes[i]['nextNodeId'] = nodes[i+1]['id']
    nodes[i]['choices'] = []
nodes[-1]['choices'] = []

data['nodes'] = nodes

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Rewrote ch1_result_perfect.json successfully.")
