import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_night.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    print("--- ch1_night.json ---")
    for node in data['nodes'][:10]:
        print(f"{node.get('speaker', '')}: {node.get('text', '')}")

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_investigation_talk.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    print("--- ch1_investigation_talk.json ---")
    for node in data['nodes']:
        print(f"{node.get('speaker', '')}: {node.get('text', '')}")
