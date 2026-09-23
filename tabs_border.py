import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                UIHelper.AddImage(tabObj, new Color32(80, 35, 10, 255));
                Button tabBtn = tabObj.AddComponent<Button>();'''

replacement = '''                Image tabImg = UIHelper.AddImage(tabObj, new Color32(80, 35, 10, 255));
                tabImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, Color.white, new Color32(20, 10, 5, 255));
                tabImg.type = Image.Type.Sliced;
                Button tabBtn = tabObj.AddComponent<Button>();'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Tabs to use Rounded Rect Sprite with border')
else:
    print('Target not found')
