import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace('\nvoid ShowPhotosensitivityWarning()', '\n        private void ShowPhotosensitivityWarning()')

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Added private to ShowPhotosensitivityWarning!")
