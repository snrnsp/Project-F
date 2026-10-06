import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for n in data.get('nodes', []):
    if n['id'] in [10, 11, 12]:
        print(f"Node {n['id']} legacy sprite: '{n.get('characterSprite', '')}'")
