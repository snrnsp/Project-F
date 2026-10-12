import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

for filename in ['ch1_night.json', 'ch1_investigation_talk.json', 'ch1_result_perfect.json', 'ch1_resolution.json']:
    print(f"--- {filename} ---")
    filepath = f'F:/Project-F/Assets/Resources/Data/Dialogues/{filename}'
    try:
        with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            nodes = data.get('nodes', [])
            print(f"Total Nodes: {len(nodes)}")
            if len(nodes) > 0:
                print(f"Start: {nodes[0].get('text')[:50]}")
                print(f"End: {nodes[-1].get('text')[:50]}")
    except Exception as e:
        print("Error reading file")
