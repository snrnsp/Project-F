import json

filepath = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# The user wants Mina's expression in node 26 to match node 25
sprite_25 = data['nodes'][25]['characterSpriteCenter']
sprite_26 = data['nodes'][26]['characterSpriteCenter']
print(f"Node 25: {repr(sprite_25)}")
print(f"Node 26: {repr(sprite_26)}")

data['nodes'][26]['characterSpriteCenter'] = sprite_25

with open(filepath, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Modification complete.")
