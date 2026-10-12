import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    speaker = node.get('speaker', '').strip()
    if speaker == '미나':
        text = node.get('text', '').replace('\n', ' ')
        print(f"[{speaker}] {text}")
