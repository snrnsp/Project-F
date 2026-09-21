import json

transcript_path = r'C:\Users\Win10\.gemini\antigravity\brain\a3ef1dad-ea8a-410f-98b8-2500b643311c\.system_generated\logs\transcript_full.jsonl'

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        if 'Story JSON File 4' in line:
            obj = json.loads(line)
            content = obj.get('content', '')
            if content:
                # Save to ch1_morning.json
                # The content has a header.
                start = content.find('{\n  \"dialogueId\"')
                if start != -1:
                    with open(r'Assets\Resources\Data\Dialogues\ch1_morning_recovered.json', 'w', encoding='utf-8') as out:
                        out.write(content[start:])
        if 'Story JSON Files 5 to 12' in line:
            obj = json.loads(line)
            content = obj.get('content', '')
            if content:
                # We need to split by '=== X. '
                parts = content.split('===')
                for part in parts:
                    if 'ch1_prologue.json' in part:
                        start = part.find('{')
                        with open(r'Assets\Resources\Data\Dialogues\ch1_prologue_recovered.json', 'w', encoding='utf-8') as out:
                            out.write(part[start:])
                    if 'ch1_incident.json' in part:
                        start = part.find('{')
                        with open(r'Assets\Resources\Data\Dialogues\ch1_incident_recovered.json', 'w', encoding='utf-8') as out:
                            out.write(part[start:])
                    if 'ch1_pre_deduction.json' in part:
                        start = part.find('{')
                        with open(r'Assets\Resources\Data\Dialogues\ch1_pre_deduction_recovered.json', 'w', encoding='utf-8') as out:
                            out.write(part[start:])
                    if 'ch1_investigation_talk.json' in part:
                        start = part.find('{')
                        with open(r'Assets\Resources\Data\Dialogues\ch1_investigation_talk_recovered.json', 'w', encoding='utf-8') as out:
                            out.write(part[start:])
                    if 'ch1_result_perfect.json' in part:
                        start = part.find('{')
                        with open(r'Assets\Resources\Data\Dialogues\ch1_result_perfect_recovered.json', 'w', encoding='utf-8') as out:
                            out.write(part[start:])
                    if 'ch1_result_fail.json' in part:
                        start = part.find('{')
                        with open(r'Assets\Resources\Data\Dialogues\ch1_result_fail_recovered.json', 'w', encoding='utf-8') as out:
                            out.write(part[start:])
