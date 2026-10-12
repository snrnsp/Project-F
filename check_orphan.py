import json
import codecs
import glob

for filepath in glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json'):
    with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    count = 0
    for i, node in enumerate(data.get('nodes', [])):
        speaker = str(node.get('speaker', '')).strip()
        sprites = [node.get('characterSpriteLeft', ''), node.get('characterSpriteCenter', ''), node.get('characterSpriteRight', ''), node.get('characterSprite', '')]
        
        # If narrator, and no sprites specified
        if not speaker and all(not s for s in sprites):
            # Check if previous node had sprites
            if i > 0:
                prev = data['nodes'][i-1]
                prev_sprites = [prev.get('characterSpriteLeft', ''), prev.get('characterSpriteCenter', ''), prev.get('characterSpriteRight', ''), prev.get('characterSprite', '')]
                if any(prev_sprites):
                    count += 1
    
    if count > 0:
        print(f"{filepath.split('/')[-1]}: {count} orphan narrator nodes")
