import json

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data.get('nodes', []):
    id = n['id']
    if id == 20:
        n['characterSpriteLeft'] = 'Characters/카스미/찡그림'
        n['characterSpriteCenter'] = 'Characters/리나/기본'
        n['characterSpriteRight'] = 'Characters/세이카/웃음'
    elif id == 21:
        n['characterSpriteLeft'] = 'Characters/카스미/찡그림'
        n['characterSpriteCenter'] = 'Characters/리나/기본'
        n['characterSpriteRight'] = 'Characters/세이카/웃음'
    elif id == 22:
        n['characterSpriteLeft'] = 'Characters/카스미/찡그림'
        n['characterSpriteCenter'] = 'Characters/리나/웃음'
        n['characterSpriteRight'] = 'Characters/세이카/웃음'

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated ch0_gathering.json successfully')
