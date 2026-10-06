import json, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

for file in glob.glob('Assets/Resources/Data/Dialogues/*.json'):
    if 'test' in file: continue
    with open(file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    print(f"--- {file} ---")
    active_sprites = {'L': '', 'C': '', 'R': ''}
    for node in data['nodes']:
        speaker = node.get('speaker', '')
        L = node.get('characterSpriteLeft', '')
        C = node.get('characterSpriteCenter', '')
        R = node.get('characterSpriteRight', '')
        
        # update active
        if L != '': active_sprites['L'] = L
        if C != '': active_sprites['C'] = C
        if R != '': active_sprites['R'] = R
        
        # If node has explicit sprite definitions but the speaker isn't one of them
        # or if the speaker is talking but isn't on screen at all!
        if speaker and speaker not in ['서하유', '선임 변호사', '경찰']:
            on_screen = False
            for pos, path in active_sprites.items():
                if speaker in path:
                    on_screen = True
            if not on_screen:
                print(f"Node {node['id']}: [{speaker}] is speaking but not on screen! Active: {active_sprites}")
