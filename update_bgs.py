import json
import os

def update_file(filename, updates):
    with open(filename, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    changed = False
    for node in data.get('nodes', []):
        nid = node['id']
        if nid in updates:
            node['backgroundSprite'] = updates[nid]
            changed = True
            
    if changed:
        with open(filename, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Updated {filename}")

update_file('Assets/Resources/Data/Dialogues/ch0_origin.json', {
    0: 'Images/bg_basement_archive',
    25: 'Images/bg_city_night',
    42: 'Images/bg_basement_archive',
    56: 'Images/bg_city_night',
    61: 'Images/bg_mansion_night'
})

update_file('Assets/Resources/Data/Dialogues/ch0_gathering.json', {
    0: 'Images/bg_mansion_night'
})

update_file('Assets/Resources/Data/Dialogues/ch0_opening.json', {
    0: 'Images/bg_city_night',
    8: 'Images/bg_agency_interior_night'
})

update_file('Assets/Resources/Data/Dialogues/ch1_morning.json', {
    0: 'Images/bg_agency_interior_morning'
})

update_file('Assets/Resources/Data/Dialogues/ch1_night.json', {
    0: 'Images/bg_city_night',
    8: 'Images/bg_abandoned_practice_room'
})

for file in ['ch1_investigation_talk.json', 'ch1_resolution.json', 'ch1_result_fail.json', 'ch1_result_perfect.json']:
    update_file(f'Assets/Resources/Data/Dialogues/{file}', {
        0: 'Images/bg_abandoned_practice_room',
        100: 'Images/bg_abandoned_practice_room' # for investigation_talk
    })

update_file('Assets/Resources/Data/Dialogues/ch1_epilogue.json', {
    0: 'Images/bg_agency_interior_morning',
    15: 'Images/bg_agency_interior_morning',
    46: 'Images/bg_agency_interior_night',
    49: 'Images/bg_abandoned_practice_room'
})

print("Done updating backgrounds!")
