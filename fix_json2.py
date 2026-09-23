import json

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data.get('nodes', []):
    id = n['id']
    if id == 14:
        n['characterSpriteLeft'] = 'Characters/세이카/웃음'
        n['characterSpriteCenter'] = ''
        n['characterSpriteRight'] = 'Characters/카스미/기본'

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated ch0_gathering.json successfully')
