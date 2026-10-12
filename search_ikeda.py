import json
import codecs
import os
import glob

with codecs.open('search_ikeda_out.txt', 'w', encoding='utf-8') as out_f:
    files = glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json')
    for filepath in files:
        with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
            try:
                data = json.load(f)
                for node in data.get('nodes', []):
                    text = node.get('text', '').replace('\n', ' ')
                    if '이케다' in text or '저택' in text or '지하실' in text:
                        out_f.write(f"{os.path.basename(filepath)} [{node['id']}] {text}\n")
            except Exception as e:
                pass
