import json
import codecs

# Fix ch0_origin.json
filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    if node['id'] == 27:
        node['command'] = 'START_DIALOGUE:ch0_gathering'

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# Fix ch1_resolution.json
filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    if node['nextNodeId'] == -1 and node.get('command') == 'END':
        node['command'] = 'START_DIALOGUE:ch1_epilogue'

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# Fix ch1_epilogue.json
filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    if node['nextNodeId'] == -1 and node.get('command') == 'END':
        node['command'] = 'CHANGE_PHASE:Lobby'

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Fixed dialogue chaining commands.")
