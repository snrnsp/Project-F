import json

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch1_morning.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data.get('nodes', []):
    id = n['id']
    if id == 25:
        n['characterSpriteLeft'] = 'Characters/리나/찡그림'
        n['characterSpriteCenter'] = 'Characters/미나/기본'
        n['characterSpriteRight'] = 'Characters/리리스/기본'
        n['slideIn'] = True
    elif id == 26:
        n['characterSpriteLeft'] = 'Characters/리나/찡그림'
        n['characterSpriteCenter'] = 'Characters/미나/기본'
        n['characterSpriteRight'] = 'Characters/리리스/기본'
    elif id == 27:
        n['characterSpriteLeft'] = 'Characters/리나/화남'
        n['characterSpriteCenter'] = 'Characters/미나/기본'
        n['characterSpriteRight'] = 'Characters/리리스/기본'
    elif id == 28:
        n['characterSpriteLeft'] = 'Characters/리나/화남'
        n['characterSpriteCenter'] = 'Characters/미나/웃음'
        n['characterSpriteRight'] = 'Characters/리리스/기본'

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated ch1_morning.json successfully')
