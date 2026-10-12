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

report = []

for filepath in files:
    filename = os.path.basename(filepath)
    if '_legacy' in filepath: continue
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    nodes = data.get('nodes', [])
    prev_sprites = {'Left': '', 'Center': '', 'Right': ''}
    prev_bg = ''
    
    for i, node in enumerate(nodes):
        speaker = node.get('speaker', '').strip()
        bg = node.get('backgroundSprite', '')
        
        sprites = {
            'Left': get_char_name(node.get('characterSpriteLeft', '')),
            'Center': get_char_name(node.get('characterSpriteCenter', '')),
            'Right': get_char_name(node.get('characterSpriteRight', ''))
        }
        
        # 1. Speaker missing from screen
        if speaker and speaker != '???' and speaker not in ['시스템', '네버모어', '주민', '경찰', '라디오', '전화', '목소리']:
            if speaker not in sprites.values() and any(sprites.values()):
                report.append(f"[{filename}] Node {node.get('id', i)}: {speaker} is speaking but not on screen! Sprites: {sprites}")
        
        # Scene changed?
        scene_changed = bg != prev_bg and bg != ''
        
        # 2. Position jumps
        if not scene_changed:
            for pos, char in sprites.items():
                if char:
                    for prev_pos, prev_char in prev_sprites.items():
                        if char == prev_char and pos != prev_pos:
                            report.append(f"[{filename}] Node {node.get('id', i)}: {char} jumped from {prev_pos} to {pos}!")
        
        prev_sprites = sprites
        if bg: prev_bg = bg

with open('sprite_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))
print(f"Found {len(report)} issues.")
