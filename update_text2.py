import json

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    if node['id'] == 45:
        node['text'] = "\"유령의 집에서 탐정 놀이?\"\n\"보수는요?\"\n\"경력에 도움이 돼요?\""

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Updated Node 45 with standard newline')
