import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_night.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for i, node in enumerate(data.get('nodes', [])):
    speaker = node.get('speaker', '').strip()
    if speaker not in ['', '세이카', '카스미', '리나', '미나', '리리스', '하루카', '서하유']:
        print(f"Unknown speaker in ch1_night: '{speaker}' at node {node['id']}")
