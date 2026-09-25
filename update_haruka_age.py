import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = 'age = "19세",'
replacement = 'age = "19세(최연소)",'

# It might be part of Haruka's profile only. Let's make sure we only replace Haruka's if there are multiple.
# Actually, Haruka is the only one with 19세. Let's just do a string replace.

if target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Haruka age')
else:
    print('Target not found')
