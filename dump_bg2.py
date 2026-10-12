import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

with codecs.open('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

nodes = data.get('nodes', [])
for node in nodes[:15]:
    print(f"Node {node['id']}: BG: {node.get('backgroundSprite', 'N/A')} Text: {node['text']}")
