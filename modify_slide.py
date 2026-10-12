import json

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

node = data['nodes'][10]
print(f"Old node: {node}")
node['slideIn'] = True
node['slideFromRight'] = True
print(f"New node: {node}")

with open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Modification complete.")
