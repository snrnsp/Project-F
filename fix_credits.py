import json
import codecs

# 1. ch1_resolution.json
filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Find node 139 (credits) and remove it
new_nodes = []
for node in data.get('nodes', []):
    if node['id'] == 139:
        continue # skip
    if node['id'] == 138:
        node['nextNodeId'] = 140 # link directly to next
    new_nodes.append(node)

data['nodes'] = new_nodes

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Removed credits from ch1_resolution.json")

# 2. ch1_epilogue.json
filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    if '사차지' in node.get('text', ''):
        node['speaker'] = '' # empty string to trigger fullscreen narrator
        node['backgroundSprite'] = 'bg_black' # use black background
        # Also wait for bgm? We can stop bgm
        node['command'] = 'AUDIO:STOP_BGM'

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Updated credits in ch1_epilogue.json")
