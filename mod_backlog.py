import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/BacklogUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('private void ShowBacklog()', 'public void ShowBacklog()')
text = text.replace('public void ToggleBacklog()', 'public bool IsOpen => backlogPanel != null && backlogPanel.activeSelf;\n\n        public void ToggleBacklog()')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Exposed ShowBacklog and IsOpen in BacklogUI')
