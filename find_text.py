import os
import json

def find_text():
    dir_path = 'F:/Project-F/Assets/Resources/Data/Dialogues'
    for file in os.listdir(dir_path):
        if not file.endswith('.json'): continue
        filepath = os.path.join(dir_path, file)
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                for i, node in enumerate(data.get('nodes', [])):
                    if '특별히 머물러' in node.get('text', ''):
                        print(f"Found in {file} at node {i}")
                        print(node['text'])
        except Exception as e:
            pass

find_text()
