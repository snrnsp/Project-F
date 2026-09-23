import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/BacklogUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('private void HideBacklog()', 'public void HideBacklog()')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Made HideBacklog public')
