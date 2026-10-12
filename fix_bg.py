import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    if node['id'] == 0:
        node['backgroundSprite'] = "Images/bg_agency_interior_night"
        break

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Updated ch0_gathering.json Node 0 background!")
