import json

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    if 22 <= int(node.get('id', -1)) <= 33:
        print(f"ID {node.get('id')}: {node.get('text')}")
