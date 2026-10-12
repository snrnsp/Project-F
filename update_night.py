import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_night.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    text = node.get('text', '')
    if '노을시 외곽에 버려진 건물' in text:
        node['text'] = text.replace('노을시 외곽에 버려진 건물', '구시가지의 낡은 상가 건물 지하실')
    if '건물 전체가 미세하게' in text:
        node['text'] = text.replace('건물 전체가', '지하실 전체가')

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Updated ch1_night.json")
