import json

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_opening.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data['nodes']:
    if n['id'] == 0:
        n['backgroundSprite'] = 'Images/city_night'
        break

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated background in ch0_opening.json')
