import json
import os

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues'
for file in os.listdir(path):
    if file.endswith('.json'):
        filepath = os.path.join(path, file)
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            try:
                data = json.load(f)
                for node in data.get('nodes', []):
                    if '이걸 어디서 구하셨습니까' in node.get('text', ''):
                        print(f"Found in {file}, Node {node.get('id')}")
                        print(f"Left: {node.get('characterSpriteLeft')}")
                        print(f"Center: {node.get('characterSpriteCenter')}")
                        print(f"Right: {node.get('characterSpriteRight')}")
            except:
                pass
