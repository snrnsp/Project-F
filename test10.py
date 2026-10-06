import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for node in data['nodes']:
    if '단순한 우연은 아닐지도' in node.get('text', '') or '잊힌 적' in node.get('text', ''):
        print(node['text'])
