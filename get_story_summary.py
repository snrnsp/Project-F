import json
import os

def summarize_file(filepath):
    if not os.path.exists(filepath):
        return f"{filepath} not found."
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    summary = []
    for node in data.get('nodes', []):
        speaker = node.get('speaker', '')
        text = node.get('text', '').replace('\n', ' ')
        if speaker or text:
            summary.append(f"[{speaker}] {text}")
    return '\n'.join(summary[:30]) + '\n... (truncated)'

with open('story_summary.txt', 'w', encoding='utf-8') as f:
    f.write('--- ch0_origin ---\n')
    f.write(summarize_file('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_origin.json') + '\n')
    f.write('--- ch0_gathering ---\n')
    f.write(summarize_file('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json') + '\n')
    f.write('--- ch0_opening ---\n')
    f.write(summarize_file('F:/Project-F/Assets/Resources/Data/Dialogues/ch0_opening.json') + '\n')
