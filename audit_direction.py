import json
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Collect all available assets
def get_assets(path):
    assets = []
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.png') or file.endswith('.jpg'):
                    # Convert to Resources path (no extension)
                    rel_path = os.path.relpath(os.path.join(root, file), 'Assets/Resources')
                    rel_path = rel_path.replace('\\', '/')
                    assets.append(os.path.splitext(rel_path)[0])
    return set(assets)

backgrounds = get_assets('Assets/Resources/Images')
characters = get_assets('Assets/Resources/Characters')

errors = []
warnings = []

# Character name to typical sprite folder mapping
char_mapping = {
    '세이카': '세이카',
    '카스미': '카스미',
    '리나': '리나',
    '리리스': '리리스',
    '미나': '미나',
    '하루카': '하루카',
    '서하유': None, # No sprite expected
    '아버지': None
}

for file in sorted(glob.glob('Assets/Resources/Data/Dialogues/*.json')):
    if 'test' in file: continue
    with open(file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    nodes = {n['id']: n for n in data.get('nodes', [])}
    
    for node in nodes.values():
        nid = node['id']
        speaker = node.get('speaker', '').strip()
        bg = node.get('backgroundSprite', '').strip()
        L = node.get('characterSpriteLeft', '').strip()
        C = node.get('characterSpriteCenter', '').strip()
        R = node.get('characterSpriteRight', '').strip()
        
        # Check missing background
        if bg and bg not in backgrounds:
            errors.append(f"[{os.path.basename(file)} Node {nid}] Missing background: {bg}")
            
        # Check missing characters
        for s, pos in [(L, 'Left'), (C, 'Center'), (R, 'Right')]:
            if s and s not in characters:
                errors.append(f"[{os.path.basename(file)} Node {nid}] Missing character sprite ({pos}): {s}")
                
        # Check if speaker is missing from screen
        if speaker and char_mapping.get(speaker):
            expected_folder = f"Characters/{char_mapping[speaker]}"
            if not any(expected_folder in s for s in [L, C, R]):
                warnings.append(f"[{os.path.basename(file)} Node {nid}] Speaker '{speaker}' is talking but their sprite might not be on screen! L: {L}, C: {C}, R: {R}")
                
        # Check for sudden layout shifts (if speaker was L in prev node, are they suddenly R?)
        # A bit hard without sequential traversal, but we can just do basic checks.

print(f"--- ERRORS ({len(errors)}) ---")
for e in errors[:50]: print(e)
print(f"--- WARNINGS ({len(warnings)}) ---")
for w in warnings[:50]: print(w)
