import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the cross character
text = text.replace('UIHelper.AddText(closeTextObj, \"\u2715\", Color.white, 24, TextAlignmentOptions.Center);', 'UIHelper.AddText(closeTextObj, \"X\", Color.white, 24, TextAlignmentOptions.Center);')
text = text.replace('UIHelper.AddText(closeTextObj, \"✕\", Color.white, 24, TextAlignmentOptions.Center);', 'UIHelper.AddText(closeTextObj, \"X\", Color.white, 24, TextAlignmentOptions.Center);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed Extra UI close button text to X')
