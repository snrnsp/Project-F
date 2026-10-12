import json
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)['nodes']
for n in data:
    if n['id'] in [24, 25, 26, 27]:
        print(f"Node {n['id']} Speaker: {n.get('speaker')} Text: {n.get('text')[:30]}")
