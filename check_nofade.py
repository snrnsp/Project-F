import json

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

print(f"Node 26 noFade: {data['nodes'][26].get('noFade')}")
