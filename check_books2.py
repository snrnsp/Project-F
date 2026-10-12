import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_investigation_talk.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    text = node.get('text', '').replace('\n', ' ')
    if '서재' in text or '책장' in text:
        print(f"[{node['id']}] {text}")
