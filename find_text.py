import json
import glob

for f in glob.glob('c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/*.json'):
    with open(f, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
        for node in data.get('nodes', []):
            if '유령의 집에서 탐정 놀이?' in node.get('text', ''):
                print(f'{f}: Node {node["id"]}')
