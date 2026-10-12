import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    speaker = node.get('speaker', '').strip()
    if speaker in ['선임 변호사', '동네 할머니']:
        sprites = [node.get('characterSpriteLeft', ''), node.get('characterSpriteCenter', ''), node.get('characterSpriteRight', '')]
        print(f"[{speaker}] sprites: {sprites}")
