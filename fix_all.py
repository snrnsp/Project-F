import json
import glob

def get_base_name(path):
    if not path: return ""
    parts = path.split('/')
    if len(parts) >= 2: return parts[-2]
    return path

def fix_file(filename):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    active_slots = {'L': '', 'C': '', 'R': ''}
    current_bg = ""
    changed = False
    
    for node in data['nodes']:
        speaker = node.get('speaker', '').strip()
        L = node.get('characterSpriteLeft', '')
        C = node.get('characterSpriteCenter', '')
        R = node.get('characterSpriteRight', '')
        bg = node.get('backgroundSprite', '')
        
        # If background changes, we reset the active slots (unless it's empty which means keep bg)
        if bg and bg != current_bg:
            active_slots = {'L': '', 'C': '', 'R': ''}
            current_bg = bg
            
        new_sprites = [s for s in [L, C, R] if s]
        
        # If it's a narrator node and L,C,R are empty, they probably meant to keep characters on screen
        if not new_sprites and speaker == '':
            if 'characterSpriteLeft' in node and node['characterSpriteLeft'] == '':
                node['characterSpriteLeft'] = active_slots['L']
            if 'characterSpriteCenter' in node and node['characterSpriteCenter'] == '':
                node['characterSpriteCenter'] = active_slots['C']
            if 'characterSpriteRight' in node and node['characterSpriteRight'] == '':
                node['characterSpriteRight'] = active_slots['R']
            changed = True
            continue
            
        # Update active slots with whatever they explicitly provided
        active_slots['L'] = L
        active_slots['C'] = C
        active_slots['R'] = R

    if changed:
        with open(filename, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Fixed narrator clears in {filename}")

for file in glob.glob('Assets/Resources/Data/Dialogues/*.json'):
    if 'test' in file: continue
    fix_file(file)

print("Done!")
