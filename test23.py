import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('Assets/Resources/Data/Dialogues/ch0_origin.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    speaker = node.get('speaker', '').strip()
    if speaker and '\n' in node.get('text', ''):
        print(f"FAILED: Node {node['id']} [{speaker}] still has newline!")
print("Check complete.")
