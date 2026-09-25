import json, sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')

def read_json(fp):
    with open(fp, 'rb') as f:
        raw = f.read()
    while raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    return json.loads(raw.decode('utf-8'))

# Read ch1_prologue and ch1_incident
for name in ['ch1_prologue', 'ch1_incident']:
    fp = f'F:/Project-F/Assets/Resources/Data/Dialogues/{name}.json'
    if not os.path.exists(fp):
        print(f'{name}: NOT FOUND')
        continue
    data = read_json(fp)
    nodes = data.get('nodes', [])
    did = data.get('dialogueId', '?')
    print(f"=== {name}.json: {did} ({len(nodes)} nodes) ===")
    for n in nodes:
        nid = n.get('id', '?')
        speaker = n.get('speaker', '')
        text = n.get('text', '')[:100]
        cmd = n.get('command', '')
        choices = n.get('choices', [])
        nxt = n.get('nextNodeId', -1)
        parts = [f"  [{nid}]"]
        if speaker:
            parts.append(f"{speaker}:")
        if text:
            parts.append(text)
        if cmd:
            parts.append(f"CMD={cmd}")
        if choices:
            parts.append(f"CHOICES={[c.get('text','') for c in choices]}")
        parts.append(f"->next={nxt}")
        print(" ".join(parts))
    print()

# Read DialogueManager commands
fp = 'F:/Project-F/Assets/Scripts/Dialogue/DialogueManager.cs'
if os.path.exists(fp):
    with open(fp, 'r', encoding='utf-8-sig') as f:
        text = f.read()
    # Find command handling
    idx = text.find('ProcessCommand')
    if idx != -1:
        print("=== DialogueManager.ProcessCommand ===")
        print(text[idx:idx+2000])
    else:
        # look for command-related code
        for line in text.split('\n'):
            if 'command' in line.lower() and ('case' in line.lower() or 'if' in line.lower() or 'switch' in line.lower()):
                print(line.strip())

# Read GamePhase enum
fp = 'F:/Project-F/Assets/Scripts/Core/GamePhase.cs'
if os.path.exists(fp):
    with open(fp, 'r', encoding='utf-8-sig') as f:
        print("=== GamePhase.cs ===")
        print(f.read())

# Read how investigation objects work  
fp = 'F:/Project-F/Assets/Scripts/Investigation/InvestigationManager.cs'
if os.path.exists(fp):
    with open(fp, 'r', encoding='utf-8-sig') as f:
        text = f.read()
    print("=== InvestigationManager (first 2000 chars) ===")
    print(text[:2000])

# Check what dialogue files the game start actually loads
fp = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
if os.path.exists(fp):
    with open(fp, 'r', encoding='utf-8-sig') as f:
        text = f.read()
    print("=== LobbyUI.cs (first 2000 chars) ===")
    print(text[:2000])
