import json
import codecs

def replace_bg(filepath, replacements):
    with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    modified = False
    for node in data.get('nodes', []):
        bg = node.get('backgroundSprite', '')
        if bg in replacements:
            node['backgroundSprite'] = replacements[bg]
            modified = True
            
    if modified:
        with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Fixed backgrounds in {filepath}")
    else:
        print(f"No changes needed in {filepath}")

# ch0_gathering.json
replace_bg(
    'F:/Project-F/Assets/Resources/Data/Dialogues/ch0_gathering.json',
    {'bg_city_night': 'Images/bg_city_night'}
)

# ch1_epilogue.json
replace_bg(
    'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json',
    {
        'bg_office_night': 'Images/bg_agency_interior_night',
        'bg_office_day': 'Images/bg_agency_interior_morning',
        'bg_black': 'Images/bg_black'
    }
)
