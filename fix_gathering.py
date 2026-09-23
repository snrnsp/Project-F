import json

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    node_id = int(node.get('id', -1))
    if 23 <= node_id <= 32:
        node['characterSpriteLeft'] = "Characters/리리스/기본"
        node['characterSpriteRight'] = "Characters/세이카/기본"
        if 'characterSpriteCenter' in node:
            del node['characterSpriteCenter']
        if 'characterSprite' in node:
            del node['characterSprite']

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Updated ch0_gathering.json Nodes 23-32")
