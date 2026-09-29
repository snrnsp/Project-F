import json

path = 'F:/Project-F/Assets/Resources/Data/Dialogues/ch1_epilogue.json'
with open(path, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

updates = {
    2: {"Left": "", "Center": "Characters/하루카/미소", "Right": ""},
    3: {"Left": "Characters/하루카/미소", "Center": "", "Right": "Characters/세이카/웃음"},
    5: {"Left": "Characters/리나/찡그림", "Center": "", "Right": "Characters/카스미/기본"},
    6: {"Left": "Characters/리나/기본", "Center": "", "Right": "Characters/카스미/기본"},
    7: {"Left": "Characters/리나/기본", "Center": "", "Right": "Characters/카스미/찡그림"},
    8: {"Left": "Characters/리나/측은", "Center": "", "Right": "Characters/카스미/기본"},
    10: {"Left": "", "Center": "Characters/리리스/기본", "Right": ""},
    11: {"Left": "", "Center": "Characters/리리스/기본", "Right": ""},
    13: {"Left": "", "Center": "Characters/리리스/기본", "Right": ""},
    14: {"Left": "", "Center": "Characters/리리스/놀람", "Right": ""},
    15: {"Left": "", "Center": "Characters/리리스/놀람", "Right": ""},
    17: {"Left": "", "Center": "Characters/리리스/눈 감음", "Right": ""},
    19: {"Left": "Characters/하루카/측은", "Center": "", "Right": "Characters/리나/기본"},
    20: {"Left": "Characters/하루카/기본", "Center": "", "Right": "Characters/리나/찡그림"},
    21: {"Left": "Characters/하루카/기본", "Center": "", "Right": "Characters/리나/찡그림"},
    22: {"Left": "Characters/하루카/기본", "Center": "", "Right": "Characters/리나/기본"},
    23: {"Left": "Characters/하루카/놀람", "Center": "", "Right": "Characters/리나/웃음"},
    24: {"Left": "Characters/하루카/웃음", "Center": "", "Right": "Characters/리나/웃음"},
    26: {"Left": "Characters/하루카/기본", "Center": "", "Right": "Characters/리나/웃음"},
    27: {"Left": "Characters/하루카/당황", "Center": "", "Right": "Characters/리나/웃음"},
    28: {"Left": "Characters/하루카/홍조", "Center": "", "Right": "Characters/리나/웃음"},
    29: {"Left": "Characters/미나/미소", "Center": "", "Right": "Characters/하루카/당황"},
    30: {"Left": "Characters/미나/기본", "Center": "", "Right": "Characters/하루카/당황"},
    31: {"Left": "Characters/미나/음침", "Center": "", "Right": "Characters/하루카/기본"},
    32: {"Left": "Characters/미나/기본", "Center": "", "Right": "Characters/카스미/기본"},
    33: {"Left": "Characters/미나/음침", "Center": "", "Right": "Characters/카스미/기본"},
    34: {"Left": "Characters/미나/기본", "Center": "", "Right": "Characters/카스미/찡그림"},
    35: {"Left": "Characters/미나/찡그림", "Center": "", "Right": "Characters/카스미/기본"},
    37: {"Left": "", "Center": "Characters/카스미/기본", "Right": ""},
    38: {"Left": "", "Center": "Characters/카스미/찡그림", "Right": ""},
    39: {"Left": "", "Center": "Characters/카스미/기본", "Right": ""},
    40: {"Left": "", "Center": "Characters/카스미/측은", "Right": ""},
    42: {"Left": "", "Center": "Characters/카스미/미소", "Right": ""},
    43: {"Left": "Characters/카스미/기본", "Center": "", "Right": "Characters/세이카/기본"},
    44: {"Left": "Characters/카스미/기본", "Center": "", "Right": "Characters/세이카/웃음"},
    46: {"Left": "", "Center": "Characters/세이카/음침", "Right": ""},
    47: {"Left": "", "Center": "Characters/세이카/기본", "Right": ""},
    52: {"Left": "", "Center": "Characters/세이카/기본", "Right": ""},
    53: {"Left": "", "Center": "Characters/세이카/웃음", "Right": ""}
}

changed = 0
for node in data['nodes']:
    speaker = node.get('speaker', '').strip()
    if speaker:
        if not node.get('characterSpriteLeft') and not node.get('characterSpriteCenter') and not node.get('characterSpriteRight'):
            nid = node['id']
            if nid in updates:
                node['characterSpriteLeft'] = updates[nid]['Left']
                node['characterSpriteCenter'] = updates[nid]['Center']
                node['characterSpriteRight'] = updates[nid]['Right']
                changed += 1

with open(path, 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Updated {changed} nodes.")
