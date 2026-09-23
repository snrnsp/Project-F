import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the SetField from the wrong place
text = text.replace('UIHelper.SetField(ui, "flashbackOverlay", flashbackObj);', '')

# 2. Add it to the correct place
target = 'UIHelper.SetField(ui, "backgroundImage", backgroundImage);'
replacement = 'UIHelper.SetField(ui, "backgroundImage", backgroundImage);\n            UIHelper.SetField(ui, "flashbackOverlay", dialoguePanelRoot.transform.Find("FlashbackOverlay").gameObject);'
text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Moved flashbackOverlay SetField below ui declaration')
