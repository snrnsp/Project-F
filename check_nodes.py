import json
import codecs
import glob

for filepath in glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json'):
    with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    nodes = data.get('nodes', [])
    node_ids = {n['id'] for n in nodes}
    filename = filepath.split('/')[-1]
    
    for node in nodes:
        next_id = node.get('nextNodeId', -1)
        if next_id != -1 and next_id not in node_ids:
            print(f"[{filename}] Node {node['id']} has invalid nextNodeId {next_id}")
        
        for choice in node.get('choices', []):
            target = choice.get('targetNodeId', -1)
            if target != -1 and target not in node_ids:
                print(f"[{filename}] Choice in Node {node['id']} points to invalid target {target}")
