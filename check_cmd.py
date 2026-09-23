import json

files = ['c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json', 
         'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json']

for f in files:
    with open(f, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
        cmd = data['nodes'][0].get('command', '')
        print(f'{f}: Node 0 command = {cmd}')
