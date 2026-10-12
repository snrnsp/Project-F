import json

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

with open('debug_epilogue.txt', 'w', encoding='utf-8') as f:
    for node in data.get('nodes', []):
        if node['id'] == 68:
            f.write(node['text'])
