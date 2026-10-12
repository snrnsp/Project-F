import json
import codecs

files = [
    'ch0_origin.json', 'ch0_gathering.json', 'ch0_opening.json', 
    'ch1_morning.json', 'ch1_night.json', 'ch1_investigation_talk.json', 
    'ch1_result_perfect.json', 'ch1_epilogue.json'
]

for filename in files:
    filepath = f'F:/Project-F/Assets/Resources/Data/Dialogues/{filename}'
    with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    # Check if sequential
    ids = [n['id'] for n in data['nodes']]
    expected = list(range(len(ids)))
    if ids != expected:
        print(f"Fixing {filename}")
        for i in range(len(data['nodes'])):
            data['nodes'][i]['id'] = i
        for i in range(len(data['nodes']) - 1):
            data['nodes'][i]['nextNodeId'] = data['nodes'][i+1]['id']
        data['nodes'][-1]['nextNodeId'] = -1
        with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        print(f"OK: {filename}")
