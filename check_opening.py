import json
import codecs

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_opening.json'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    last_node = data['nodes'][-1]
    print(f"Last node id: {last_node['id']}")
    print(f"Command: {last_node.get('command')}")
    print(f"NextNodeId: {last_node.get('nextNodeId')}")
