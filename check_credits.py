import json
import codecs
import sys

sys.stdout.reconfigure(encoding='utf-8')

def check_file(filepath):
    try:
        with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        for node in data.get('nodes', []):
            if '사차지' in node.get('text', ''):
                print(f"[{filepath}] Node {node['id']}: {node['text']}")
    except Exception as e:
        pass

check_file('F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json')
check_file('F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json')
