import json
import os
import glob

def get_base_name(path):
    if not path: return None
    parts = path.split('/')
    if len(parts) >= 2: return parts[-2]
    return path

def compute_targets(owner):
    result = [0.25, 0.5, 0.75]
    used = []
    for s in range(3):
        if owner[s] is not None:
            used.append(s)
            
    if len(used) == 1: xs = [0.5]
    elif len(used) == 2: xs = [0.25, 0.75]
    else: xs = [0.20, 0.50, 0.80]
    
    for i in range(len(used)):
        s = used[i]
        target = xs[i]
        if owner[s] == '리나':
            if target < 0.5: target += 0.05
            elif target > 0.5: target -= 0.05
        result[s] = target
    return result

dialogue_files = glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json')
dialogue_files = [f for f in dialogue_files if '_legacy' not in f]

for filepath in dialogue_files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f).get('nodes', [])
        
    active_speakers = {}
    last_target_x = [-1.0, -1.0, -1.0]
    
    for node in data:
        req = [
            node.get('characterSpriteLeft') or None,
            node.get('characterSpriteCenter') or None,
            node.get('characterSpriteRight') or None
        ]
        
        new_names = set()
        new_owner = [None, None, None]
        for s in range(3):
            if not req[s]: continue
            name = get_base_name(req[s])
            if name in new_names:
                req[s] = None
                continue
            new_owner[s] = name
            new_names.add(name)
            
        prev_owner = [None, None, None]
        prev_slot_of = {}
        for name, s in active_speakers.items():
            prev_owner[s] = name
            prev_slot_of[name] = s
            
        target_x = compute_targets(new_owner)
        
        active_speakers.clear()
        
        for s in range(3):
            name = new_owner[s]
            old = prev_owner[s]
            
            if name is None:
                continue
                
            active_speakers[name] = s
            
            if name in prev_slot_of:
                from_slot = prev_slot_of[name]
                if from_slot != s:
                    print(f"[{filename}] Node {node['id']}: {name} moved slot from {from_slot} to {s}. targetX: {target_x[s]}")
                else:
                    if abs(last_target_x[s] - target_x[s]) > 0.01 and last_target_x[s] >= 0:
                        print(f"[{filename}] Node {node['id']}: {name} slided in same slot {s} from {last_target_x[s]} to {target_x[s]}")
            else:
                # newly entering
                pass
                
        for s in range(3):
            if new_owner[s] is not None:
                last_target_x[s] = target_x[s]
            else:
                last_target_x[s] = -1.0
