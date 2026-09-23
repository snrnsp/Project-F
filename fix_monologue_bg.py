import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = 'img.color = new Color(0, 0, 0, 0.75f); // Semi-transparent black background'
replacement = 'img.color = new Color(0, 0, 0, 1f); // Solid black background for monologue'

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated monologue background to solid black')
