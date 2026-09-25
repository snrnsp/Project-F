import json

path = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json'

with open(path, 'r', encoding='utf-8-sig') as f:
    raw = f.read()
    while raw.startswith('\ufeff'):
        raw = raw[1:]
    data = json.loads(raw)

for node in data['nodes']:
    if node['id'] == 5:
        node['text'] = '"세이카 씨, 우리 로펌의 주요 고객 중에 노을시 경찰청 관계자가 있다는 거 알지? 이 건은 더 이상 건드리지 마."\n\n선임은 단호하게 세이카의 말을 끊었다.'
        print('Node 5 updated.')

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('File saved.')
