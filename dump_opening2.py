import json
import codecs
import sys

# Windows console output encoding fix
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_opening.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    text = node.get('text', '').replace('\n', ' ')
    print(f"[{node['id']}] {node.get('speaker', '')}: {text}")
