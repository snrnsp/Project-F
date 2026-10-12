import json
import codecs
import os
import glob

with codecs.open('search_books_out.txt', 'w', encoding='utf-8') as out_f:
    files = glob.glob('F:/Project-F/Assets/Resources/Data/Dialogues/*.json')
    for filepath in files:
        with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
            try:
                data = json.load(f)
                for node in data.get('nodes', []):
                    text = node.get('text', '').replace('\n', ' ')
                    if '책' in text or '서재' in text or '단서' in text or '빠져' in text or '찾아줘' in text:
                        out_f.write(f"{os.path.basename(filepath)} [{node['id']}] {text}\n")
            except Exception as e:
                pass
