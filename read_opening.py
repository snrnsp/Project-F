import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_opening.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

with codecs.open('opening_out.txt', 'w', encoding='utf-8') as f:
    for node in data['nodes']:
        speaker = node.get('speaker', '')
        text = node.get('text', '').replace('\n', ' ')
        if speaker or text:
            f.write(f"[{node['id']}] [{speaker}] {text}\n")
