import json, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')

all_sprites = set()
for root, _, files in os.walk('Assets/Resources/Characters'):
    for f in files:
        if f.endswith('.png'):
            # e.g. Assets/Resources/Characters/카스미/기본.png -> Characters/카스미/기본
            rel = os.path.relpath(os.path.join(root, f), 'Assets/Resources')
            rel = rel.replace('\\', '/')
            all_sprites.add(rel[:-4])

print(f"Total sprites found: {len(all_sprites)}")

missing = set()
for file in glob.glob('Assets/Resources/Data/Dialogues/*.json'):
    with open(file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    for node in data['nodes']:
        for k in ['characterSpriteLeft', 'characterSpriteCenter', 'characterSpriteRight', 'characterSprite']:
            s = node.get(k, '')
            if s and s not in all_sprites:
                missing.add(s)

if missing:
    print("MISSING SPRITES:")
    for m in missing: print(m)
else:
    print("No missing sprites found!")
