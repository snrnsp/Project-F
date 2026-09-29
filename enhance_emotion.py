import json, sys, os

sys.stdout.reconfigure(encoding='utf-8')
base = 'F:/Project-F/Assets/Resources/Data/Dialogues'

# ============================================================
# Fix 1: ch1_resolution.json - Haruka's empathy + Seika's notebook
# ============================================================
path = os.path.join(base, 'ch1_resolution.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

nodes = data['nodes']

# --- Fix 1a: Enhance Haruka piano scene ---
# Find the node "하루카의 손 아래에서, 건반이 따뜻해졌다."
warm_idx = -1
for i, n in enumerate(nodes):
    if '건반이 따뜻해졌다' in n.get('text', ''):
        warm_idx = i
        break

if warm_idx >= 0:
    # Insert Haruka's empathy BEFORE the warmth moment
    empathy_nodes = [
        {
            "speaker": " ",
            "text": "하루카는 알고 있었다.\n투명인간 취급을 받으며, 아무도 자신을 봐주지 않는 교실에서 혼자 도시락을 먹던 그 끔찍한 추위를.",
            "command": ""
        },
        {
            "speaker": "하루카",
            "text": "(떨리는 목소리로) ...알아요. 아무도 나를 봐주지 않을 때... 이 작은 건반들만이 유일한 세상이었을 거라는 거...",
            "command": ""
        },
        {
            "speaker": " ",
            "text": "하루카의 눈에서 눈물이 떨어져 건반 위로 번졌다.",
            "command": ""
        },
    ]
    for j, en in enumerate(empathy_nodes):
        en['characterSpriteLeft'] = ''
        en['characterSpriteCenter'] = ''
        en['characterSpriteRight'] = ''
        en['backgroundSprite'] = ''
        en['choices'] = []
        en['id'] = 0
        en['nextNodeId'] = 0
        nodes.insert(warm_idx + j, en)
    
    # Now fix the warmth node text to be more emotional
    new_warm_idx = warm_idx + len(empathy_nodes)
    nodes[new_warm_idx]['text'] = '그 순간 — 얼음장 같던 건반 아래에서, 희미한 온기가 배어 나왔다.'
    
    # Fix Haruka's reaction after warmth
    for n in nodes[new_warm_idx:]:
        if n.get('speaker') == '하루카' and '따뜻해요' in n.get('text', ''):
            n['text'] = '...따뜻해요. 건반이... 따뜻해요. 울고 있어요... 이 사람...'
            break
    
    print('Fix 1a: Enhanced Haruka piano scene')

# --- Fix 1b: Enhance Seika's notebook scene ---
for i, n in enumerate(nodes):
    if n.get('speaker') == '세이카' and '이 사람이 존재했다는 것을' in n.get('text', ''):
        # Replace with more emotional version
        nodes.insert(i, {
            "speaker": "세이카",
            "text": "세상이 당신의 이름을 지운다 해도... 이 작은 수첩의 잉크마저 지우진 못할 거야.",
            "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
            "backgroundSprite": "", "choices": [], "id": 0, "nextNodeId": 0, "command": ""
        })
        # Update the original node
        nodes[i+1]['text'] = '이 사람이 존재했다는 것을 — 우리 여섯 명이, 여기에 영원히 기억한다.'
        print('Fix 1b: Enhanced Seika notebook scene')
        break

# --- Fix 1c: Add Rina's frustration-to-sadness ---
for i, n in enumerate(nodes):
    if n.get('speaker') == '리나' and '다음에는 반드시 이름까지' in n.get('text', ''):
        # Insert Rina's vulnerability before her vow
        nodes.insert(i, {
            "speaker": "리나",
            "text": "......주먹으로 때려서 해결할 수 있는 거였으면 좋겠는데.",
            "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
            "backgroundSprite": "", "choices": [], "id": 0, "nextNodeId": 0, "command": ""
        })
        nodes.insert(i+1, {
            "speaker": " ",
            "text": "리나가 코끝을 문질렀다. 눈이 빨개져 있었다.",
            "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
            "backgroundSprite": "", "choices": [], "id": 0, "nextNodeId": 0, "command": ""
        })
        print('Fix 1c: Added Rina vulnerability')
        break

# Re-index all nodes
for i, n in enumerate(nodes):
    n['id'] = i
    n['nextNodeId'] = i + 1 if i < len(nodes) - 1 else -1

data['nodes'] = nodes
with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Saved ch1_resolution.json (' + str(len(nodes)) + ' nodes)')

# ============================================================
# Fix 2: ch1_epilogue.json - Liris decoding + Pumpkin cookie
# ============================================================
path = os.path.join(base, 'ch1_epilogue.json')
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

nodes = data['nodes']

# --- Fix 2a: Enhance Liris decoding moment ---
for i, n in enumerate(nodes):
    if n.get('speaker') == '리리스' and "'...고마워.'" in n.get('text', ''):
        # Change the delivery
        n['text'] = "'...고, 마워...'"
        # Insert Liris's emotional crack before
        nodes.insert(i, {
            "speaker": "리리스",
            "text": "디코딩하면... 잠깐. 이건...",
            "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
            "backgroundSprite": "", "choices": [], "id": 0, "nextNodeId": 0, "command": ""
        })
        nodes.insert(i+1, {
            "speaker": " ",
            "text": "항상 무미건조하던 리리스의 눈동자가, 모니터 불빛 아래서 아주 미세하게 흔들렸다.",
            "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
            "backgroundSprite": "", "choices": [], "id": 0, "nextNodeId": 0, "command": ""
        })
        print('Fix 2a: Enhanced Liris decoding moment')
        break

# --- Fix 2b: Enhance cookie scene ---
for i, n in enumerate(nodes):
    if '이번에는 아무도 듣는 이가 없었다' in n.get('text', ''):
        n['text'] = '이번에는 아무도 듣는 이가 없었다.\n하지만 피아노 위에는, 어젯밤 하루카가 몰래 올려두고 간 작은 호박 쿠키 하나가 놓여 있었다.'
        print('Fix 2b: Added pumpkin cookie detail')
    if '하지만 그 선율은' in n.get('text', '') and '슬프지 않았다' in n.get('text', ''):
        # Insert a bridge node before
        nodes.insert(i, {
            "speaker": "",
            "text": "누군가 자신을 기억해준다는 것. 그 작은 온기 하나로 충분하다는 듯 —",
            "characterSpriteLeft": "", "characterSpriteCenter": "", "characterSpriteRight": "",
            "backgroundSprite": "", "choices": [], "id": 0, "nextNodeId": 0, "command": ""
        })
        # Update the original
        nodes[i+1]['text'] = '어둠 속으로 번져가는 선율은, 더 이상 슬프지 않았다.'
        print('Fix 2b2: Enhanced cookie scene ending')
        break

# Re-index all nodes
for i, n in enumerate(nodes):
    n['id'] = i
    n['nextNodeId'] = i + 1 if i < len(nodes) - 1 else -1

data['nodes'] = nodes
with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Saved ch1_epilogue.json (' + str(len(nodes)) + ' nodes)')

print('\nAll emotional enhancements applied!')
