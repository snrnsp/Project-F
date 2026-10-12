import json
import sys

transcript_path = 'C:/Users/cccc0/.gemini/antigravity/brain/fc10953b-5038-4aaf-8269-364bd034e7f8/.system_generated/logs/transcript.jsonl'

try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in reversed(lines):
        data = json.loads(line)
        if data.get('type') == 'PLANNER_RESPONSE':
            if 'content' in data:
                print(data['content'])
                sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
