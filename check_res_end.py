import json
import codecs
import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_resolution.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

for node in data.get('nodes', [])[-5:]:
    speaker = node.get('speaker', '').strip()
    text = node.get('text', '').replace('\n', ' ')
    cmd = node.get('command', '')
    print(f"[{speaker}] {text} (cmd: {cmd})")
