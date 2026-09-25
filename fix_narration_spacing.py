import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

def load_json(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        raw = f.read()
        while raw.startswith('\ufeff'):
            raw = raw[1:]
        return json.loads(raw)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

base = 'F:/Project-F/Assets/Resources/Data/Dialogues'
total_fixes = 0

for root, dirs, files in os.walk(base):
    for file in files:
        if file.endswith('.json'):
            path = os.path.join(root, file)
            try:
                data = load_json(path)
                modified = False
                for node in data.get('nodes', []):
                    # Check if it's a narration node (no speaker)
                    speaker = node.get('speaker', '').strip()
                    text = node.get('text', '')
                    
                    if not speaker and '\n\n' in text:
                        node['text'] = text.replace('\n\n', '\n')
                        modified = True
                        total_fixes += 1
                
                if modified:
                    save_json(path, data)
                    print(f'✅ Updated {file}')
            except Exception as e:
                print(f'Error processing {file}: {e}')

print(f'\n═══ 총 {total_fixes}건 내레이션 노드 간격 수정 완료 ═══')
