import json
import os

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    if '특별히 머물러' in node.get('text', ''):
        old_text = node['text']
        node['text'] = old_text.replace('크큭', '크흠')
        print(f"Changed: {old_text} -> {node['text']}")

with open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Modification complete.")
