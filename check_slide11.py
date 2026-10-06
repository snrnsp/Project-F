import json
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data.get('nodes', []):
    if n['id'] == 11:
        print(f"Node 11 slideIn: {n.get('slideIn')}, slideFromRight: {n.get('slideFromRight')}")
