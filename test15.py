import json, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

for file in glob.glob('Assets/Resources/Data/Dialogues/*.json'):
    if 'test' in file: continue
    with open(file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    for node in data['nodes']:
        L = node.get('characterSpriteLeft', '')
        C = node.get('characterSpriteCenter', '')
        R = node.get('characterSpriteRight', '')
        sprites = [s for s in [L, C, R] if s]
        names = []
        for s in sprites:
            parts = s.split('/')
            name = parts[-2] if len(parts) >= 2 else s
            names.append(name)
        if len(names) != len(set(names)):
            print(f"{file} Node {node['id']} has duplicates! Sprites: {sprites}")
