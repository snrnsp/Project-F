import json
import codecs
import os
import glob

with codecs.open('search_location_out.txt', 'w', encoding='utf-8') as out_f:
    files = glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json')
    for filepath in files:
        with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
            try:
                data = json.load(f)
                for node in data.get('nodes', []):
                    text = node.get('text', '').replace('\n', ' ')
                    if any(x in text for x in ['언덕', '이케다', '학원', '건물', '지하실', '저택']):
                        out_f.write(f"{os.path.basename(filepath)} [{node['id']}] {text}\n")
            except Exception as e:
                pass
