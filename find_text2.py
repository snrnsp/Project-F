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
                    if '경찰이 안 움직이면 내가 직접' in node.get('text', ''):
                        print(f"Found in {file} at node {i}")
        except Exception as e:
            pass

find_text()
