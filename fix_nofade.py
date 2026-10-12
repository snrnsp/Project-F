import json
import glob
import os

files = glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json')
fixes = 0

for filepath in files:
    filename = os.path.basename(filepath)
    if '_legacy' in filepath: continue
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    nodes = data.get('nodes', [])
    prev_sprites = {'Left': '', 'Center': '', 'Right': ''}
    prev_bg = ''
    
    for i, node in enumerate(nodes):
        bg = node.get('backgroundSprite', '')
        sprites = {
            'Left': node.get('characterSpriteLeft', ''),
            'Center': node.get('characterSpriteCenter', ''),
            'Right': node.get('characterSpriteRight', '')
        }
        
        scene_changed = bg != prev_bg and bg != ''
        
        if not scene_changed and sprites == prev_sprites and any(sprites.values()):
            if not node.get('noFade', False) and not node.get('command'):
                node['noFade'] = True
                fixes += 1
                
        prev_sprites = sprites
        if bg: prev_bg = bg

    with open(filepath, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Added noFade=true to {fixes} nodes!")
