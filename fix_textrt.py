import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                // Tab text - Make it a child of TabContainer so it perfectly centers in the visible area!
                GameObject tabTextObj = UIHelper.CreateUIObject("Text", tabContainerObj.transform);
                RectTransform textRt = tabTextObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(textRt);
                // Shift text up slightly within the container so it's vertically balanced
                textRt.offsetMin = new Vector2(0, 5);
                textRt.offsetMax = new Vector2(0, 5);
                TextMeshProUGUI tabText = UIHelper.AddText(tabTextObj, charNames[ci], new Color32(60, 40, 20, 255), 18, TextAlignmentOptions.Center);'''

replacement = '''                // Tab text - Make it a child of TabContainer so it perfectly centers in the visible area!
                GameObject tabTextObj = UIHelper.CreateUIObject("Text", tabContainerObj.transform);
                RectTransform tabTextRt = tabTextObj.GetComponent<RectTransform>();
                UIHelper.StretchFull(tabTextRt);
                // Shift text up slightly within the container so it's vertically balanced
                tabTextRt.offsetMin = new Vector2(0, 5);
                tabTextRt.offsetMax = new Vector2(0, 5);
                TextMeshProUGUI tabText = UIHelper.AddText(tabTextObj, charNames[ci], new Color32(60, 40, 20, 255), 18, TextAlignmentOptions.Center);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Renamed textRt to tabTextRt')
else:
    print('Target not found')
