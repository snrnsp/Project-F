import json
import codecs
import glob
import sys
sys.stdout.reconfigure(encoding='utf-8')

for filepath in glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json'):
    with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    filename = filepath.split('/')[-1]
    for node in data.get('nodes', []):
        speaker = node.get('speaker', '').strip()
        if speaker not in ['', '세이카', '카스미', '리나', '미나', '리리스', '하루카', '서하유']:
            print(f"Unknown speaker in {filename}: '{speaker}' at node {node['id']}")
