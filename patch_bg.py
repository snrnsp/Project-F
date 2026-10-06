import json

path = 'Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    if node['id'] == 23:
        if node['backgroundSprite'] == 'Images/bg_mansion_night':
            node['backgroundSprite'] = 'Images/bg_agency_interior_night'
            print("Changed Node 23 background to Images/bg_agency_interior_night")

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
