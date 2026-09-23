import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('private void CreateLanguageUI')
start = max(0, idx - 100)
print(text[start:idx+1000])
