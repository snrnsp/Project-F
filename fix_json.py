import json

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch1_morning.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data.get('nodes', []):
    id = n['id']
    if id == 12:
        n['characterSpriteLeft'] = 'Characters/카스미/황당'
        n['characterSpriteCenter'] = ''
        n['characterSpriteRight'] = 'Characters/하루카/기본'
    elif id == 13:
        n['characterSpriteLeft'] = 'Characters/카스미/황당'
        n['characterSpriteCenter'] = 'Characters/리나/웃음'
        n['characterSpriteRight'] = 'Characters/하루카/기본'
    elif id == 14:
        n['characterSpriteLeft'] = 'Characters/카스미/찡그림'
        n['characterSpriteCenter'] = 'Characters/리나/웃음'
        n['characterSpriteRight'] = 'Characters/하루카/기본'
    elif id == 15:
        n['characterSpriteLeft'] = 'Characters/카스미/찡그림'
        n['characterSpriteCenter'] = 'Characters/리나/기본'
        n['characterSpriteRight'] = 'Characters/하루카/기본'
    elif id == 16:
        n['characterSpriteLeft'] = 'Characters/카스미/찡그림'
        n['characterSpriteCenter'] = 'Characters/리나/기본'
        n['characterSpriteRight'] = 'Characters/하루카/웃음'
    elif id == 17:
        n['characterSpriteLeft'] = 'Characters/카스미/찡그림'
        n['characterSpriteCenter'] = 'Characters/리나/웃음'
        n['characterSpriteRight'] = 'Characters/하루카/삐짐'

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated ch1_morning.json successfully')
