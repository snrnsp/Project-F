import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_investigation_talk.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

print("Final node:")
print(data['nodes'][-1])
