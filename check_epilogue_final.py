import json
import codecs
import sys

sys.stdout.reconfigure(encoding='utf-8')

with codecs.open('F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    for node in data['nodes'][-5:]:
        print(f"Node {node['id']}: speaker='{node.get('speaker')}' / {node.get('text')} / bg='{node.get('backgroundSprite')}'")
