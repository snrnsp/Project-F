import json, csv, sys, os

sys.stdout.reconfigure(encoding='utf-8')

in_dir = 'F:/Project-F/Assets/Resources/Data/Dialogues'
csv_path = 'F:/Project-F/Story_Export.csv'

# Read CSV
csv_data = {}  # key: (filename, node_id) -> {speaker, text, background, command}
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        fname = row['Chapter/File']
        nid = row['Node ID']
        # Convert speaker back
        speaker = row['Speaker']
        if speaker == '(대사창 내레이션)':
            speaker = ' '
        elif speaker == '(전체화면 내레이션)':
            speaker = ''
        csv_data[(fname, nid)] = {
            'speaker': speaker,
            'text': row['Text'],
            'background': row['Background'],
            'command': row['Command']
        }

# Read each JSON and compare
files = [
    'ch0_origin.json', 'ch0_gathering.json', 'ch0_opening.json',
    'ch1_morning.json', 'ch1_night.json', 'ch1_investigation_talk.json',
    'ch1_result_perfect.json', 'ch1_result_fail.json', 'ch1_epilogue.json'
]

diffs = []
for fname in files:
    full = os.path.join(in_dir, fname)
    if not os.path.exists(full):
        continue
    with open(full, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    for node in data.get('nodes', []):
        nid = str(node.get('id', ''))
        key = (fname, nid)
        if key not in csv_data:
            diffs.append(f"MISSING IN CSV: {fname} node {nid}")
            continue
        
        csv_row = csv_data[key]
        
        # Compare text
        json_text = node.get('text', '')
        csv_text = csv_row['text']
        if json_text != csv_text:
            diffs.append(f"TEXT DIFF: {fname} node {nid}")
            diffs.append(f"  JSON: {json_text[:80]}...")
            diffs.append(f"  CSV:  {csv_text[:80]}...")
        
        # Compare speaker
        json_speaker = node.get('speaker', '')
        csv_speaker = csv_row['speaker']
        if json_speaker != csv_speaker:
            diffs.append(f"SPEAKER DIFF: {fname} node {nid}: JSON='{json_speaker}' CSV='{csv_speaker}'")
        
        # Compare background
        json_bg = node.get('backgroundSprite', '')
        csv_bg = csv_row['background']
        if json_bg != csv_bg:
            diffs.append(f"BG DIFF: {fname} node {nid}: JSON='{json_bg}' CSV='{csv_bg}'")
        
        # Compare command
        json_cmd = node.get('command', '')
        csv_cmd = csv_row['command']
        if json_cmd != csv_cmd:
            diffs.append(f"CMD DIFF: {fname} node {nid}: JSON='{json_cmd}' CSV='{csv_cmd}'")

if not diffs:
    print("NO DIFFERENCES FOUND")
else:
    for d in diffs:
        print(d)
