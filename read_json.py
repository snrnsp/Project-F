import json
import codecs
import sys

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

files = ['c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json',
         'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json']

for f in files:
    try:
        with open(f, 'r', encoding='utf-8-sig') as file:
            data = json.load(file)
            print('---', f.split('/')[-1], '---')
            texts = [f"[{node.get('speaker', 'Narrator')}] {node.get('text', '')}" for node in data.get('nodes', [])]
            for t in texts[:20]:
                print(t)
            print('... (truncated)')
    except Exception as e:
        print('Error reading', f, ':', e)
