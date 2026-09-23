import codecs

path = 'c:/Users/cccc0/Documents/Project-F/ProjectSettings/ProjectSettings.asset'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('activeInputHandler: 2', 'activeInputHandler: 1')
text = text.replace('activeInputHandler: 0', 'activeInputHandler: 1')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated activeInputHandler to 1 (Input System Package)')
