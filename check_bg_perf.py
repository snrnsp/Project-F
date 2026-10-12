import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_result_perfect.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    bg = node.get('backgroundSprite', '')
    if bg:
        print(f"[{node['id']}] {bg}")
