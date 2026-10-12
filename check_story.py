import json
import codecs
import glob
import sys
sys.stdout.reconfigure(encoding='utf-8')

files = [
    'ch0_origin.json',
    'ch0_gathering.json',
    'ch0_opening.json',
    'ch1_morning.json',
    'ch1_night.json',
    'ch1_investigation_talk.json',
    'ch1_result_perfect.json',
    'ch1_resolution.json',
    'ch1_epilogue.json'
]

for filename in files:
    filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/' + filename
    with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        print(f"\n--- {filename} ---")
        for node in data.get('nodes', [])[:3]:  # Print first 3 nodes
            speaker = node.get('speaker', '').strip()
            text = node.get('text', '').replace('\n', ' ')
            print(f"[{speaker}] {text}")
        print("...")
        for node in data.get('nodes', [])[-3:]: # Print last 3 nodes
            speaker = node.get('speaker', '').strip()
            text = node.get('text', '').replace('\n', ' ')
            print(f"[{speaker}] {text}")
