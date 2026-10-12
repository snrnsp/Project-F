import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for i, node in enumerate(data.get('nodes', [])):
    speaker = str(node.get('speaker', '')).strip()
    sprites = [node.get('characterSpriteLeft', ''), node.get('characterSpriteCenter', ''), node.get('characterSpriteRight', '')]
    if not speaker and not any(sprites):
        if i > 0:
            print(f"Node {node['id']}: {node.get('text', '')}")
