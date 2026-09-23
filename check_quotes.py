with open('c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    stripped = line.rstrip('\r\n')
    temp = stripped.replace('\\' + '"', '')
    if temp.count('"') % 2 == 1:
        print(f'Line {i+1} has odd quotes: {stripped[:100]}')
