import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

text = text.replace('UIHelper.AddText(tabTextObj, charNames[ci], Color.black, 30, TextAlignmentOptions.Center);', 
                    'UIHelper.AddText(tabTextObj, charNames[ci], Color.black, 45, TextAlignmentOptions.Center);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)
print("Updated tab text font size to 45")
