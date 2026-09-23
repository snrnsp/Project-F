import codecs
import json

path1 = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json'
with open(path1, 'r', encoding='utf-8-sig') as f:
    data1 = json.load(f)

for node in data1['nodes']:
    if node['id'] == 15:
        node['backgroundSprite'] = 'Images/bg_flashback'

with open(path1, 'w', encoding='utf-8-sig') as f:
    json.dump(data1, f, ensure_ascii=False, indent=2)


path2 = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(path2, 'r', encoding='utf-8-sig') as f:
    data2 = json.load(f)

for node in data2['nodes']:
    if node['id'] == 0:
        node['backgroundSprite'] = 'Images/bg_flashback'

with open(path2, 'w', encoding='utf-8-sig') as f:
    json.dump(data2, f, ensure_ascii=False, indent=2)

print('Updated both flashback JSON files to use abstract dark background')
