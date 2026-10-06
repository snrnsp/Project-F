import json

def get_base_name(path):
    if not path: return ""
    parts = path.split('/')
    if len(parts) >= 2: return parts[-2]
    return path

def fix_file(filename, start_node_id=0):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    active_slots = {'L': '', 'C': '', 'R': ''}
    
    # Pre-fill active slots by scanning up to start_node_id
    for node in data['nodes']:
        if node['id'] < start_node_id:
            L = node.get('characterSpriteLeft', '')
            C = node.get('characterSpriteCenter', '')
            R = node.get('characterSpriteRight', '')
            if L: active_slots['L'] = L
            elif 'characterSpriteLeft' in node: active_slots['L'] = ''
            if C: active_slots['C'] = C
            elif 'characterSpriteCenter' in node: active_slots['C'] = ''
            if R: active_slots['R'] = R
            elif 'characterSpriteRight' in node: active_slots['R'] = ''
        else:
            break

    for node in data['nodes']:
        if node['id'] < start_node_id: continue
        
        speaker = node.get('speaker', '').strip()
        L = node.get('characterSpriteLeft', '')
        C = node.get('characterSpriteCenter', '')
        R = node.get('characterSpriteRight', '')
        
        # If the node has explicit sprite requests, and it's not just a blank narrator node
        # Wait, the subagent wrote blank narrator nodes L:'', C:'', R:''.
        # And for speakers, it wrote C:'Characters/Speaker/Expression', L:'', R:''.
        # This completely destroys the previous state.
        
        # We will override the node's L, C, R based on a maintained active_slots state!
        
        # Who is supposed to be on screen?
        new_sprites = [s for s in [L, C, R] if s]
        
        if not new_sprites and speaker == '':
            # Narrator node. Just keep previous state!
            node['characterSpriteLeft'] = active_slots['L']
            node['characterSpriteCenter'] = active_slots['C']
            node['characterSpriteRight'] = active_slots['R']
            continue
            
        if speaker and speaker not in ['서하유', '선임 변호사', '경찰']:
            # A character is speaking.
            # Are they in new_sprites?
            speaker_sprite = next((s for s in new_sprites if speaker in s), None)
            if not speaker_sprite:
                # Fallback to 기본 if not provided
                speaker_sprite = f"Characters/{speaker}/기본"
                
            # We want to keep existing characters on screen, but add the speaker if they aren't there.
            # And maybe remove someone if there are > 3.
            
            # 1. Update active_slots with existing characters
            # But wait, if the subagent put them in C, we should put them in their PREVIOUS slot if they had one!
            prev_slot = None
            for k, v in active_slots.items():
                if get_base_name(v) == speaker:
                    prev_slot = k
                    break
            
            if prev_slot:
                active_slots[prev_slot] = speaker_sprite
            else:
                # Need to find an empty slot
                empty_slots = [k for k, v in active_slots.items() if not v]
                if empty_slots:
                    active_slots[empty_slots[0]] = speaker_sprite
                else:
                    # Replace someone (e.g. L)
                    active_slots['L'] = speaker_sprite
            
            node['characterSpriteLeft'] = active_slots['L']
            node['characterSpriteCenter'] = active_slots['C']
            node['characterSpriteRight'] = active_slots['R']
            continue
            
        # If it's 서하유 or others who don't have sprites, just keep state
        node['characterSpriteLeft'] = active_slots['L']
        node['characterSpriteCenter'] = active_slots['C']
        node['characterSpriteRight'] = active_slots['R']

    with open(filename, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

fix_file('Assets/Resources/Data/Dialogues/ch1_resolution.json', 89)
fix_file('Assets/Resources/Data/Dialogues/ch1_epilogue.json', 0)
print("Fixed!")
