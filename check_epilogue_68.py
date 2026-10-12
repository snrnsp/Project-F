import json

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    if node['id'] == 68:
        print(f"Node 68 text: {repr(node['text'])}")
