import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_morning.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    text = node.get('text', '')
    if '폐쇄 음악학원' in text:
        node['text'] = text.replace('폐쇄 음악학원', '버려진 민간 상가 건물 지하실')
    if '폐쇄된 음악학원' in text:
        node['text'] = text.replace('폐쇄된 음악학원', '버려진 상가 지하실')
    if '건물 진동' in text:
        node['text'] = text.replace('건물 진동', '지하철 진동')

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Updated ch1_morning.json")
