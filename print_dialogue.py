import json
data = json.load(open('Assets/Resources/Data/Dialogues/ch0_gathering.json', encoding='utf-8-sig'))
with open('out.txt', 'w', encoding='utf-8') as f:
    for n in data['nodes']:
        if 0 <= n['id'] <= 35:
            f.write(f"Node {n['id']} [BG:{n.get('backgroundSprite','')}]: {n['speaker']} - {n['text']}\n")
