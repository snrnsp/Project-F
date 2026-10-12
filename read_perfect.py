import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_result_perfect.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    for node in data['nodes']:
        print(f"{node.get('speaker', '')}: {node.get('text', '')}".replace('\n', ' '))
