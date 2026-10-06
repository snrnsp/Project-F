import json
import glob
import sys
sys.stdout.reconfigure(encoding='utf-8')

bg_set = set()
for file in glob.glob('Assets/Resources/Data/Dialogues/*.json'):
    if 'test' in file: continue
    with open(file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    for node in data.get('nodes', []):
        bg = node.get('backgroundSprite', '').strip()
        if bg:
            bg_set.add(bg)

print("Unique backgrounds requested in JSONs:")
for bg in sorted(bg_set):
    print(bg)
