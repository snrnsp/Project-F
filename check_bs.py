import json
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)['nodes']
for n in data:
    if n['id'] in [25, 26]:
        for key in ['characterSpriteLeft', 'characterSpriteCenter', 'characterSpriteRight']:
            val = n.get(key) or ''
            if '\\' in val:
                print('BACKSLASH FOUND IN', val)
