import json
import codecs
import glob
import sys
sys.stdout.reconfigure(encoding='utf-8')

for filepath in glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json'):
    with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        bgs = set()
        for node in data.get('nodes', []):
            bg = node.get('backgroundSprite')
            if bg:
                bgs.add(bg)
        if bgs:
            print(f"{filepath.split('/')[-1]}: {bgs}")
