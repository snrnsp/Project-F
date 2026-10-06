import json
with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# Node 26
data['nodes'][26]['characterSpriteLeft'] = 'Characters/카스미/찡그림'
data['nodes'][26]['characterSpriteCenter'] = 'Characters/미나/기본'
data['nodes'][26]['characterSpriteRight'] = ''

# Node 27
data['nodes'][27]['characterSpriteLeft'] = 'Characters/카스미/찡그림'
data['nodes'][27]['characterSpriteCenter'] = 'Characters/미나/기본'
data['nodes'][27]['characterSpriteRight'] = ''

# Node 28
data['nodes'][28]['characterSpriteLeft'] = 'Characters/카스미/찡그림'
data['nodes'][28]['characterSpriteCenter'] = 'Characters/미나/기본'
data['nodes'][28]['characterSpriteRight'] = ''

# Node 29
data['nodes'][29]['characterSpriteLeft'] = 'Characters/세이카/기본'
data['nodes'][29]['characterSpriteCenter'] = 'Characters/미나/비웃음'
data['nodes'][29]['characterSpriteRight'] = ''

# Node 30
data['nodes'][30]['characterSpriteLeft'] = 'Characters/세이카/기본'
data['nodes'][30]['characterSpriteCenter'] = 'Characters/미나/홍조'
data['nodes'][30]['characterSpriteRight'] = ''

with open('Assets/Resources/Data/Dialogues/ch0_gathering.json', 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Patched Mina position!")
