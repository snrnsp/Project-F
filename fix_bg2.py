import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_bg = '''            // Background Image
            GameObject bgImgObj = UIHelper.CreateUIObject("BackgroundImage", dialoguePanelRoot.transform);
            UIHelper.StretchFull(bgImgObj.GetComponent<RectTransform>());
            Image backgroundImage = UIHelper.AddImage(bgImgObj, new Color(1,1,1,0));'''

new_bg = '''            // Background Image
            GameObject bgImgObj = UIHelper.CreateUIObject("BackgroundImage", dialoguePanelRoot.transform);
            UIHelper.StretchFull(bgImgObj.GetComponent<RectTransform>());
            bgImgObj.GetComponent<RectTransform>().offsetMin = new Vector2(-2, -2);
            bgImgObj.GetComponent<RectTransform>().offsetMax = new Vector2(2, 2);
            Image backgroundImage = UIHelper.AddImage(bgImgObj, new Color(1,1,1,0));'''

if old_bg in content:
    content = content.replace(old_bg, new_bg)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Added bleed to dialogue bg.")
else:
    print("Could not find Dialogue BG.")
