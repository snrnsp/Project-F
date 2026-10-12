import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    text = node.get('text', '').replace('\n', ' ')
    print(f"[{node['id']}] {node.get('speaker', '')}: {text}".encode('utf-8').decode('cp949', 'ignore'))
