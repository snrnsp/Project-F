import json, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

for file in glob.glob('Assets/Resources/Data/Dialogues/*.json'):
    if 'test' in file: continue
    with open(file, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    print(f"--- {file} ---")
    active_sprites = {'L': '', 'C': '', 'R': ''}
    for node in data['nodes']:
        speaker = node.get('speaker', '').strip()
        L = node.get('characterSpriteLeft', '')
        C = node.get('characterSpriteCenter', '')
        R = node.get('characterSpriteRight', '')
        
        # update active
        if L != '': active_sprites['L'] = L
        if C != '': active_sprites['C'] = C
        if R != '': active_sprites['R'] = R
        
        if L == 'clear': active_sprites['L'] = ''
        if C == 'clear': active_sprites['C'] = ''
        if R == 'clear': active_sprites['R'] = ''
        
        # if the node provides empty strings, it does NOT clear the active sprite in the game? 
        # Actually in Unity: 
        # if (!string.IsNullOrEmpty(node.characterSpriteLeft)) leftImage.sprite = Load;
        # So empty string means KEEP PREVIOUS.
        
        if speaker and speaker not in ['서하유', '선임 변호사', '경찰', '???', '뉴스 앵커', '기자', '경찰관']:
            on_screen = False
            for pos, path in active_sprites.items():
                if speaker in path:
                    on_screen = True
            if not on_screen:
                print(f"Node {node['id']}: [{speaker}] talking but NOT on screen. Active: {active_sprites}")
