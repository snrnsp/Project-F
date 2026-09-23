import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('isUiHidden = !isUiHidden;', 'isUiHidden = !isUiHidden;\n                if (isUiHidden) StopAutoPlay();')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added StopAutoPlay to UI hide logic')
