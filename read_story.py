import json, os, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

for fp in sorted(glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/ch*.json')):
    with open(fp, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    nodes = data.get('nodes', [])
    did = data.get('dialogueId', '?')
    print(f"=== {os.path.basename(fp)}: {did} ({len(nodes)} nodes) ===")
    for n in nodes:
        nid = n.get('id', '?')
        speaker = n.get('speaker', '')
        text = n.get('text', '')[:100]
        cmd = n.get('command', '')
        choices = n.get('choices', [])
        nxt = n.get('nextNodeId', -1)
        line = f"  [{nid}] "
        if speaker:
            line += f"{speaker}: "
        if text:
            line += text
        if cmd:
            line += f"  CMD={cmd}"
        if choices:
            line += f"  CHOICES={[c.get('text','') for c in choices]}"
        line += f"  ->next={nxt}"
        print(line)
    print()

# Also read cases and evidence
for pattern in ['F:/Project-F/Assets/Resources/Data/Cases/*.json',
                'F:/Project-F/Assets/Resources/Data/Evidence/*.json']:
    for fp in sorted(glob.glob(pattern)):
        with open(fp, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        print(f"=== {os.path.basename(fp)} ===")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
        print()

# Read the test dialogue intro to understand format
fp = 'F:/Project-F/Assets/Resources/Data/Dialogues/test_dialogue_intro.json'
if os.path.exists(fp):
    with open(fp, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    print("=== test_dialogue_intro.json (FULL) ===")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
