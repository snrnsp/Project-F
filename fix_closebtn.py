import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '            UIHelper.SetField(extraUi, "closeButton", closeBtn);\n'

if target1 in text:
    # Remove from its current position
    text = text.replace(target1, '')
    
    # Insert at the bottom, right before extraUiRef = extraUi;
    target2 = '            extraUiRef = extraUi;'
    replacement2 = '            UIHelper.SetField(extraUi, "closeButton", closeBtn);\n            extraUiRef = extraUi;'
    
    text = text.replace(target2, replacement2)
    
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Moved closeButton SetField to the bottom')
else:
    print('Target not found')
