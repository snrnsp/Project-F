import sys, json
sys.stdout.reconfigure(encoding='utf-8')

path = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_result_perfect.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    raw = f.read()
    while raw.startswith('\ufeff'):
        raw = raw[1:]
    data = json.loads(raw)

nodes = data['nodes']

# Node 0: "세 개의 증거" → "다섯 개의 증거"  
for node in nodes:
    if node['id'] == 0:
        node['text'] = "완벽한 추론이다. 다섯 개의 증거가 하나의 결론을 향해 모여들고 있었다."
        print(f"  Node 0: '세 개' → '다섯 개'")

# Insert 2 new nodes after node 3 (음파 분석) and before node 4 (세이카's conclusion)
# Shift existing nodes 4+ by 2

new_nodes = []
insert_point = None

for i, node in enumerate(nodes):
    new_nodes.append(node)
    if node['id'] == 3:
        insert_point = i
        # Insert new node for footprints
        new_nodes.append({
            "id": 100,  # temp, will renumber
            "speaker": "세이카",
            "text": "바닥의 발자국은 피아노를 향해 걸어갔지만 도중에 사라졌어. 걸어가던 존재가 소멸한 거야. 물리적으로 이 공간에 있었다가 사라졌다는 움직일 수 없는 증거지.",
            "characterSpriteLeft": "",
            "characterSpriteCenter": "Characters/세이카/기본",
            "characterSpriteRight": "",
            "backgroundSprite": "",
            "choices": [],
            "nextNodeId": -1,
            "command": "",
            "slideIn": False,
            "noFade": False
        })
        # Insert new node for temperature
        new_nodes.append({
            "id": 101,  # temp
            "speaker": "세이카",
            "text": "그리고 연주 중 피아노 주변의 온도만 급격히 떨어졌다가 연주가 끝나자 회복됐어. '현상'은 물리 법칙까지 왜곡하고 있어.",
            "characterSpriteLeft": "",
            "characterSpriteCenter": "Characters/세이카/찡그림",
            "characterSpriteRight": "",
            "backgroundSprite": "",
            "choices": [],
            "nextNodeId": -1,
            "command": "",
            "slideIn": False,
            "noFade": False
        })

# Renumber all nodes sequentially and fix nextNodeId
for i, node in enumerate(new_nodes):
    node['id'] = i
    if node.get('command', '').startswith(('START_DIALOGUE', 'CHANGE_PHASE', 'END')):
        node['nextNodeId'] = -1
    elif node.get('command', '') == 'END':
        node['nextNodeId'] = -1
    elif i + 1 < len(new_nodes):
        node['nextNodeId'] = i + 1
    else:
        node['nextNodeId'] = -1

# Fix the last node which should have END command
for node in new_nodes:
    if node.get('command') == 'END':
        node['nextNodeId'] = -1

data['nodes'] = new_nodes

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ ch1_result_perfect.json: {len(nodes)}노드 → {len(new_nodes)}노드 (새 증거 2개 반영)")
