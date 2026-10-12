import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_result_perfect.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data['nodes']:
    if node['id'] == 9:
        node['text'] = "잭오가 포착한 주파수 기록... 이건 어떤 암호나 기계적인 패턴이 아니었어."
        node['speaker'] = "세이카"
    if node['id'] == 10:
        node['text'] = "불규칙하게 건반을 내리친 흔적들. 누구라도 좋으니 자기를 알아달라는 절박한 발버둥... '나를 찾아달라'는 메시지야."
        node['speaker'] = "세이카"

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Updated ch1_result_perfect.json")
