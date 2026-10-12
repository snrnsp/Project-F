import codecs
import json
import glob
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

for file in glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json'):
    if '_legacy' in file: continue
    with codecs.open(file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    prev_slots = {}
    changed = False
    for i, node in enumerate(data['nodes']):
        sprites = {
            'Left': node.get('characterSpriteLeft', ''),
            'Center': node.get('characterSpriteCenter', ''),
            'Right': node.get('characterSpriteRight', '')
        }
        
        active_count = sum(1 for v in sprites.values() if v)
        
        if active_count == 1:
            # Find which slot has the character and who it is
            slot, sprite = next((k, v) for k, v in sprites.items() if v)
            base_name = sprite.split('/')[-2] if '/' in sprite else sprite
            
            # Where were they previously?
            prev_slot = prev_slots.get(base_name)
            
            # If they were somewhere else previously, or they were nowhere and not in Center
            target_slot = slot
            if prev_slot:
                target_slot = prev_slot
            else:
                target_slot = 'Center'
                
            if target_slot != slot:
                print(f"{os.path.basename(file)} Node {node['id']}: Moving {base_name} from {slot} to {target_slot}")
                node['characterSpriteLeft'] = ''
                node['characterSpriteCenter'] = ''
                node['characterSpriteRight'] = ''
                node['characterSprite' + target_slot] = sprite
                changed = True
        
        # Update prev_slots for the NEXT node
        prev_slots.clear()
        if node.get('characterSpriteLeft'): prev_slots[node['characterSpriteLeft'].split('/')[-2] if '/' in node['characterSpriteLeft'] else node['characterSpriteLeft']] = 'Left'
        if node.get('characterSpriteCenter'): prev_slots[node['characterSpriteCenter'].split('/')[-2] if '/' in node['characterSpriteCenter'] else node['characterSpriteCenter']] = 'Center'
        if node.get('characterSpriteRight'): prev_slots[node['characterSpriteRight'].split('/')[-2] if '/' in node['characterSpriteRight'] else node['characterSpriteRight']] = 'Right'
        
    if changed:
        with codecs.open(file, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
