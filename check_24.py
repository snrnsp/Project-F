import json
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)['nodes']
for n in data:
    if n['id'] == 24:
        print(f"Node 24 nextNodeId: {n['nextNodeId']}")
