import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    if node['id'] == 13: # The node where it says "며칠 뒤..." or node 14
        pass
    if '며칠 뒤' in node.get('text', ''):
        node['backgroundSprite'] = 'Images/bg_law_firm_archive_night'
        print(f"Set bg_law_firm_archive_night on node {node['id']}")
    if '그해 여름' in node.get('text', ''):
        node['text'] = node['text'].replace('그해 여름,', '그해 여름 밤,')

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
