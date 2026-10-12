import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

print("Nodes in epilogue:")
print(len(data['nodes']))
