import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

def read_json(fp):
    with open(fp, 'rb') as f:
        raw = f.read()
    while raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    return json.loads(raw.decode('utf-8'))

base = 'F:/Project-F/Assets/Resources/Data/Dialogues'

print("=" * 60)
print("FULL STORY FLOW VALIDATION")
print("=" * 60)

# Track the complete flow
flow = ['ch0_origin']
visited = set()

while flow:
    current = flow[-1]
    if current in visited:
        print(f"\n[LOOP DETECTED] {current} already visited!")
        break
    visited.add(current)
    
    fp = f'{base}/{current}.json'
    if not os.path.exists(fp):
        print(f"\n[ERROR] File not found: {current}.json")
        break
    
    data = read_json(fp)
    nodes = data.get('nodes', [])
    
    # Find terminal nodes (commands)
    end_cmds = []
    for n in nodes:
        cmd = n.get('command', '')
        if cmd:
            end_cmds.append((n.get('id', '?'), cmd))
    
    print(f"\n[OK] {current}.json ({len(nodes)} nodes)")
    for nid, cmd in end_cmds:
        print(f"  Node {nid}: {cmd}")
    
    # Find next dialogue in chain
    next_dialogue = None
    for n in nodes:
        cmd = n.get('command', '')
        if cmd.startswith('START_DIALOGUE:'):
            next_dialogue = cmd.split(':')[1]
        elif cmd == 'CHANGE_PHASE:Investigation':
            print(f"  --> INVESTIGATION PHASE")
        elif cmd == 'CHANGE_PHASE:Deduction':
            print(f"  --> DEDUCTION PHASE")
        elif cmd == 'END':
            print(f"  --> END (return to lobby)")
    
    if next_dialogue:
        print(f"  --> chains to: {next_dialogue}")
        flow.append(next_dialogue)
    else:
        break

# Validate case + evidence files
print("\n" + "=" * 60)
print("CASE & EVIDENCE VALIDATION")
print("=" * 60)

case_fp = 'F:/Project-F/Assets/Resources/Data/Cases/ch1_case.json'
if os.path.exists(case_fp):
    case = read_json(case_fp)
    print(f"\nCase: {case.get('caseName', '?')}")
    for q in case.get('questions', []):
        print(f"  Q: {q['questionText']} -> {q['correctEvidenceId']}")
    print(f"  Perfect: {case.get('perfectDialogueId', '?')}")
    print(f"  Fail: {case.get('failDialogueId', '?')}")
    
    # Check result dialogues exist
    for key in ['perfectDialogueId', 'failDialogueId']:
        did = case.get(key, '')
        fp = f'{base}/{did}.json'
        exists = os.path.exists(fp)
        status = "OK" if exists else "MISSING"
        print(f"  [{status}] {did}.json")

evidence_fp = 'F:/Project-F/Assets/Resources/Data/Evidence/ch1_evidence.json'
if os.path.exists(evidence_fp):
    ev = read_json(evidence_fp)
    print(f"\nEvidence DB: {len(ev.get('evidences', []))} items")
    for e in ev.get('evidences', []):
        print(f"  - {e['id']}: {e['evidenceName']}")

print("\n" + "=" * 60)
print("ALL CHAPTER 1 FILES")
print("=" * 60)
for fn in sorted(os.listdir(base)):
    if fn.startswith('ch1') and fn.endswith('.json'):
        fp = os.path.join(base, fn)
        data = read_json(fp)
        nodes = data.get('nodes', [])
        print(f"  {fn}: {len(nodes)} nodes")

print("\n[DONE] Validation complete!")
