import sys, json, os

path = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

nodes = data['nodes']

# find index of node 27
idx = -1
for i, n in enumerate(nodes):
    if n['text'] == '「네버모어 오컬트 탐정 사무소」':
        idx = i
        break

# The next node is old 28. We will remove old 28 and insert the new ones.
nodes.pop(idx + 1)

new_nodes = [
    {
        'speaker': ' ',
        'text': '간판만큼이나 이질적인 것은 저택의 외관과 내부였다.',
        'characterSpriteLeft': '', 'characterSpriteCenter': '', 'characterSpriteRight': '',
        'backgroundSprite': '', 'choices': [], 'command': ''
    },
    {
        'speaker': ' ',
        'text': '현관에는 사시사철 불이 꺼지지 않는 거대한 잭오랜턴이 놓여 있었고, 복도와 응접실 곳곳에는 거미줄과 호박 모양의 장식들이 가득했다.',
        'characterSpriteLeft': '', 'characterSpriteCenter': '', 'characterSpriteRight': '',
        'backgroundSprite': '', 'choices': [], 'command': ''
    },
    {
        'speaker': ' ',
        'text': '1년 내내 할로윈 파티가 열리는 듯한 기괴하면서도 동화 같은, 비현실적인 풍경.',
        'characterSpriteLeft': '', 'characterSpriteCenter': '', 'characterSpriteRight': '',
        'backgroundSprite': '', 'choices': [], 'command': ''
    },
    {
        'speaker': '세이카',
        'text': '할로윈 장식? 반은 내 취향이지만, 나머지 반은 철저한 전략이야.',
        'characterSpriteLeft': 'Characters/세이카/기본', 'characterSpriteCenter': '', 'characterSpriteRight': '',
        'backgroundSprite': '', 'choices': [], 'command': ''
    },
    {
        'speaker': '세이카',
        'text': "'설명할 수 없는 기괴한 일'을 겪은 사람이 딱딱한 경찰서나 평범한 사무실을 찾아가긴 힘들잖아?",
        'characterSpriteLeft': 'Characters/세이카/기본', 'characterSpriteCenter': '', 'characterSpriteRight': '',
        'backgroundSprite': '', 'choices': [], 'command': ''
    },
    {
        'speaker': '세이카',
        'text': '하지만 애초에 이렇게 비현실적인 공간이라면... 비정상적인 이야기를 털어놓는 데 심리적인 문턱이 낮아지겠지.',
        'characterSpriteLeft': 'Characters/세이카/미소', 'characterSpriteCenter': '', 'characterSpriteRight': '',
        'backgroundSprite': '', 'choices': [], 'command': ''
    }
]

for i, n in enumerate(new_nodes):
    nodes.insert(idx + 1 + i, n)

# Inherit background from previous node if empty
bg = ''
for n in nodes:
    if 'backgroundSprite' in n and n['backgroundSprite']:
        bg = n['backgroundSprite']
    elif 'backgroundSprite' not in n:
        n['backgroundSprite'] = ''

# Re-index all
for i, n in enumerate(nodes):
    n['id'] = i
    n['nextNodeId'] = i + 1
nodes[-1]['nextNodeId'] = -1

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print('Updated ch0_origin.json')
