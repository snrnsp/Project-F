import json
import glob
import os

files = glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json')
fixes = 0

def get_char_name(sprite_path):
    if not sprite_path: return ''
    parts = sprite_path.split('/')
    if len(parts) >= 2: return parts[1]
    return ''

for filepath in files:
    filename = os.path.basename(filepath)
    if '_legacy' in filepath: continue
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    nodes = data.get('nodes', [])
    prev_names = {'Left': '', 'Center': '', 'Right': ''}
    prev_bg = ''
    
    for i, node in enumerate(nodes):
        bg = node.get('backgroundSprite', '')
        names = {
            'Left': get_char_name(node.get('characterSpriteLeft', '')),
            'Center': get_char_name(node.get('characterSpriteCenter', '')),
            'Right': get_char_name(node.get('characterSpriteRight', ''))
        }
        
        scene_changed = bg != prev_bg and bg != ''
        
        # If exactly the same characters are on the exact same positions
        if not scene_changed and names == prev_names and any(names.values()):
            if not node.get('noFade', False) and not node.get('command') and not node.get('slideIn', False):
                node['noFade'] = True
                fixes += 1
                
        prev_names = names
        if bg: prev_bg = bg

    with open(filepath, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Added noFade=true to {fixes} nodes!")
