import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for node in data['nodes']:
    if node['id'] in [30, 31, 32, 33, 34]:
        print(f"Node {node['id']}: Speaker: '{node.get('speaker', '')}' Text: '{node.get('text', '')}'")
