import json

path = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json'

with open(path, 'r', encoding='utf-8-sig') as f:
    raw = f.read()
    while raw.startswith('\ufeff'):
        raw = raw[1:]
    data = json.loads(raw)

for node in data['nodes']:
    if node['id'] == 22:
        node['text'] = '하지만 사무소를 열고 6개월이 지나도록, 의뢰인도 동료도 오지 않았다.\n\n넓은 저택에서 혼자 와인을 마시며 실종자들의 흔적을 추적하는 나날이 이어졌다.'
        print('Node 22 updated.')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('File saved.')
