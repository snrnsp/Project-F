import json
import glob

def process_file(filename):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
        
    changed = False
    for node in data.get('nodes', []):
        speaker = node.get('speaker', '').strip()
        if speaker:  # Not a monologue/narrator
            for key in ['text', 'text_en', 'text_ja', 'text_cn', 'text_tw']:
                if key in node and '\n' in node[key]:
                    # Replace newline with a space to prevent words from sticking together
                    node[key] = node[key].replace('\n', ' ')
                    # Also replace multiple spaces with single space just in case
                    node[key] = ' '.join(node[key].split())
                    changed = True
                    
    if changed:
        with open(filename, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Processed {filename}")

for file in glob.glob('Assets/Resources/Data/Dialogues/*.json'):
    process_file(file)

print("Done!")
