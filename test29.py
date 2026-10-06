import json, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

for file in glob.glob('Assets/Resources/Data/Dialogues/*.json'):
    if 'test' in file: continue
    with open(file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    print(f"\n--- {file} ---")
    for node in data.get('nodes', []):
        bg = node.get('backgroundSprite', '').strip()
        if bg:
            print(f"Node {node['id']}: {bg}")
