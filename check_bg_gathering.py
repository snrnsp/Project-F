import codecs
import json

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    bg = node.get('backgroundSprite', '')
    if bg:
        print(f"Node {node['id']}: {bg}")
