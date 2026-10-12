import json
import os
import glob

data_dir = 'F:/Project-F/Assets/Resources/Data/Dialogues'
files = glob.glob(os.path.join(data_dir, '*.json'))

def get_char_name(path):
    if not path: return ""
    parts = path.split('/')
    if len(parts) >= 2: return parts[1]
    return ""

for filepath in files:
    if '_legacy' in filepath: continue
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        
    modified = False
    
    # 1. Fix layouts
    for node in data.get('nodes', []):
        L = node.get('characterSpriteLeft', '')
        C = node.get('characterSpriteCenter', '')
        R = node.get('characterSpriteRight', '')
        
        sprites = [s for s in [L, C, R] if s]
        
        # Rule: 1 character should be Center
        if len(sprites) == 1 and not C:
            node['characterSpriteLeft'] = ''
            node['characterSpriteCenter'] = sprites[0]
            node['characterSpriteRight'] = ''
            modified = True
            
        # Rule: 2 characters should be Left and Right
        if len(sprites) == 2 and C:
            # We have Center and someone else. We want Left and Right.
            if L and C: # Left and Center -> Left and Right
                node['characterSpriteLeft'] = L
                node['characterSpriteCenter'] = ''
                node['characterSpriteRight'] = C
                modified = True
            elif C and R: # Center and Right -> Left and Right
                node['characterSpriteLeft'] = C
                node['characterSpriteCenter'] = ''
                node['characterSpriteRight'] = R
                modified = True
                
    # 2. Fix noFade flags
    prev_L = ""
    prev_C = ""
    prev_R = ""
    for node in data.get('nodes', []):
        L = node.get('characterSpriteLeft', '')
        C = node.get('characterSpriteCenter', '')
        R = node.get('characterSpriteRight', '')
        
        is_same_L = get_char_name(L) and get_char_name(L) == get_char_name(prev_L)
        is_same_C = get_char_name(C) and get_char_name(C) == get_char_name(prev_C)
        is_same_R = get_char_name(R) and get_char_name(R) == get_char_name(prev_R)
        
        # If any slot has the same character as before, we should set noFade to true
        # Wait, if ALL characters on screen were already on screen in the same slot, set noFade=true
        sprites_on_screen = [s for s in [L, C, R] if s]
        if sprites_on_screen:
            all_same = True
            if L and not is_same_L: all_same = False
            if C and not is_same_C: all_same = False
            if R and not is_same_R: all_same = False
            
            if all_same and not node.get('noFade', False):
                node['noFade'] = True
                modified = True
                
        prev_L = L
        prev_C = C
        prev_R = R

    if modified:
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Fixed {os.path.basename(filepath)}")
