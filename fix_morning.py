import json, sys
sys.stdout.reconfigure(encoding='utf-8')
fp = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_morning.json'
with open(fp, 'rb') as f:
    raw = f.read()
while raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
data = json.loads(raw.decode('utf-8'))
nodes = data['nodes']

# Find all relevant nodes near the end
for n in nodes:
    nid = n.get('id', '?')
    if nid >= 64:
        text = n.get('text', '')[:80]
        cmd = n.get('command', '')
        nxt = n.get('nextNodeId', -1)
        print(f"Node {nid}: text=[{text}] cmd=[{cmd}] next={nxt}")

# Change: node 66 should chain to ch1_night instead of ending
# Find the node with command END
for n in nodes:
    if n.get('command') == 'END':
        print(f"\nChanging node {n['id']} from END to START_DIALOGUE:ch1_night")
        n['command'] = 'START_DIALOGUE:ch1_night'
        break

# Also update the title card node to remove the "제1화 완" feel
# Node 68 has the title card "제1화: 잊혀진 피아니스트"
for n in nodes:
    if n.get('id') == 68:
        n['text'] = '— 제1화: 잊혀진 피아니스트 —'
        print(f"Updated title card node {n['id']}")

# Write back
with open(fp, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("\nDone! ch1_morning.json updated.")
