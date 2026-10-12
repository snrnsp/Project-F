import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_investigation_talk.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    for i, node in enumerate(data['nodes']):
        print(f"[{i}] {node.get('speaker', '')}: {node.get('text', '')}".replace('\n', ' '))
