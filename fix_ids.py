import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for i in range(len(data['nodes'])):
    data['nodes'][i]['id'] = i

for i in range(len(data['nodes']) - 1):
    data['nodes'][i]['nextNodeId'] = data['nodes'][i+1]['id']

data['nodes'][-1]['nextNodeId'] = -1

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print(f"Renumbered {len(data['nodes'])} nodes.")
