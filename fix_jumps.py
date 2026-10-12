import json
import glob
import os

files = glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json')

for filepath in files:
    filename = os.path.basename(filepath)
    if '_legacy' in filepath: continue
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    nodes = data.get('nodes', [])
    
    # We will do multiple passes to propagate positions backward
    changed = True
    while changed:
        changed = False
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
            
            if not scene_changed:
                for pos in ['Left', 'Center', 'Right']:
                    char_path = sprites[pos]
                    if char_path:
                        for prev_pos in ['Left', 'Center', 'Right']:
                            prev_char_path = prev_sprites[prev_pos]
                            # If same character jumped
                            if char_path == prev_char_path and pos != prev_pos:
                                # We can fix it by moving the char in the PREVIOUS node to 'pos'
                                # ONLY IF the target position was EMPTY in the previous node!
                                if prev_sprites[pos] == '':
                                    nodes[i-1]['characterSprite' + pos] = prev_char_path
                                    nodes[i-1]['characterSprite' + prev_pos] = ''
                                    # print(f"Fixed {char_path} jump from {prev_pos} to {pos} at node {i-1} in {filename}")
                                    changed = True
                                    break
                        if changed: break
            
            if changed: break
            
            prev_sprites = sprites
            if bg: prev_bg = bg

    with open(filepath, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

print("Fixed sprite jumps!")
