import json
import codecs
import os
import glob

files = glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json')
for filepath in files:
    with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
        try:
            data = json.load(f)
            for node in data.get('nodes', []):
                text = node.get('text', '').replace('\n', ' ')
                if '책' in text or '서재' in text or '빠져' in text:
                    print(f"{os.path.basename(filepath)} [{node['id']}] {text}")
        except Exception as e:
            pass
