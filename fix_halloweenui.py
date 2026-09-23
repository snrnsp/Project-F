import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('UIHelper.SetField(dialogueUi, "flashbackOverlay", flashbackObj);', 'UIHelper.SetField(ui, "flashbackOverlay", flashbackObj);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed HalloweenUIBuilder.cs')
