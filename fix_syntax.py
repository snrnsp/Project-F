import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Image bgImg = UIHelper.AddImage(extraBgBtnObj, new Color32(15, 8, 25, 200)); # Made slightly transparent so lobby is visible behind', 'Image bgImg = UIHelper.AddImage(extraBgBtnObj, new Color32(15, 8, 25, 200)); // Made slightly transparent so lobby is visible behind')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed syntax error')
