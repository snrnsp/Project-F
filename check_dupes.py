import json
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)['nodes']
ids = [n['id'] for n in data]
from collections import Counter
counts = Counter(ids)
for k, v in counts.items():
    if v > 1:
        print(f"Duplicate ID: {k}")
print("Done checking duplicates.")
