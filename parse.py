import json
import glob

files = ["ch1_night.json", "ch1_investigation_talk.json", "ch1_result_perfect.json", "ch1_result_fail.json"]

for f in files:
    try:
        with open('Assets/Resources/Data/Dialogues/' + f, 'r', encoding='utf-8-sig') as file:
            data = json.load(file)
            print(f'========== {f} ==========')
            for node in data.get('nodes', []):
                speaker = node.get('speaker', '')
                text = node.get('text', '')
                print(f'[{node.get("id")}] {speaker}: {text}'.replace('\n', ' '))
    except Exception as e:
        print(e)
