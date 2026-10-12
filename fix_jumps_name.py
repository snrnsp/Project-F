import json
import glob
import os

files = glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json')

def get_char_name(sprite_path):
    if not sprite_path:
        return ''
    parts = sprite_path.split('/')
    if len(parts) >= 2:
        return parts[1]
    return ''

for filepath in files:
    filename = os.path.basename(filepath)
    if '_legacy' in filepath: continue
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    nodes = data.get('nodes', [])
    
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
                        char_name = get_char_name(char_path)
                        for prev_pos in ['Left', 'Center', 'Right']:
                            prev_char_path = prev_sprites[prev_pos]
                            if prev_char_path:
                                prev_char_name = get_char_name(prev_char_path)
                                # If same character jumped
                                if char_name == prev_char_name and pos != prev_pos:
                                    # We can fix it by moving the char in the PREVIOUS node to 'pos'
                                    # ONLY IF the target position was EMPTY in the previous node!
                                    if prev_sprites[pos] == '':
                                        nodes[i-1]['characterSprite' + pos] = prev_char_path
                                        nodes[i-1]['characterSprite' + prev_pos] = ''
                                        changed = True
                                        break
                        if changed: break
            
            if changed: break
            
            prev_sprites = sprites
            if bg: prev_bg = bg

    with open(filepath, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

print("Fixed sprite jumps by name!")
