import json
import glob
import os
from collections import OrderedDict

def get_base_name(sprite_path):
    if not sprite_path: return ''
    parts = sprite_path.split('/')
    if len(parts) >= 2: return parts[-2]
    return sprite_path

for path in glob.glob('c:/Users/cccc0/Documents/Project-F/Assets/Resources/Data/Dialogues/*.json'):
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            
        nodes = data.get('nodes', [])
        
        # We will track active characters in an OrderedDict: base_name -> (position, full_path)
        # position can be 'Left', 'Center', 'Right'
        # To handle manual overrides, if a node has >= 2 characters, we reset our tracking.
        
        active = OrderedDict()
        
        changed = False
        
        for n in nodes:
            l = n.get('characterSpriteLeft')
            c = n.get('characterSpriteCenter')
            r = n.get('characterSpriteRight')
            
            chars_in_node = []
            if l: chars_in_node.append(('Left', l))
            if c: chars_in_node.append(('Center', c))
            if r: chars_in_node.append(('Right', r))
            
            # If the node manually clears or sets multiple, trust it and reset state
            if len(chars_in_node) >= 2 or n.get('id') == 0:
                active.clear()
                for pos, sprite in chars_in_node:
                    active[get_base_name(sprite)] = (pos, sprite)
                continue
                
            # If the node has exactly 1 character, and we had >= 2 active...
            if len(chars_in_node) == 1 and len(active) >= 2:
                speaker_sprite = chars_in_node[0][1]
                speaker_name = get_base_name(speaker_sprite)
                
                # We want to KEEP the other active characters!
                new_active = OrderedDict()
                
                # Check if speaker was already on screen
                target_pos = None
                if speaker_name in active:
                    target_pos = active[speaker_name][0]
                else:
                    # Find empty slot
                    used_slots = [v[0] for v in active.values()]
                    for p in ['Left', 'Center', 'Right']:
                        if p not in used_slots:
                            target_pos = p
                            break
                    if not target_pos:
                        # Evict oldest
                        oldest = list(active.keys())[0]
                        target_pos = active[oldest][0]
                        del active[oldest]
                
                # Update speaker
                if speaker_name in active:
                    del active[speaker_name]
                active[speaker_name] = (target_pos, speaker_sprite)
                
                # Reconstruct node sprites
                n['characterSpriteLeft'] = ''
                n['characterSpriteCenter'] = ''
                n['characterSpriteRight'] = ''
                
                for name, (pos, sprite) in active.items():
                    n['characterSprite' + pos] = sprite
                    
                changed = True
            elif len(chars_in_node) == 1:
                # 1 char, but only 1 active. Just update active.
                active.clear()
                pos, sprite = chars_in_node[0]
                active[get_base_name(sprite)] = (pos, sprite)
            elif len(chars_in_node) == 0:
                # No chars in node? Keep active if it's a continuous conversation without clearing?
                # Actually if it's a narrator, it might clear. Let's just clear active.
                active.clear()

        if changed:
            with open(path, 'w', encoding='utf-8-sig') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print('Smoothed', os.path.basename(path))

    except Exception as e:
        print('Error processing', path, e)
