import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''                if (profile.name.Contains("카스미") || profile.name.Contains("Kasumi")) {'''

replacement = '''                if (profile.name.Contains("카스미") || profile.name.Contains("Kasumi") ||
                    profile.name.Contains("미나") || profile.name.Contains("Mina") ||
                    profile.name.Contains("하루카") || profile.name.Contains("Haruka")) {'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated ExtraUI to also shift Mina and Haruka portraits')
else:
    print('Target not found')
