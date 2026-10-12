import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'// Gear Icon.*?else iconText\.font = Resources\.GetBuiltinResource<Font>\("LegacyRuntime\.ttf"\);'

replacement = r'''// Hamburger Icon (Font-independent to fix WebGL invisible gear issue)
            for(int j=0; j<3; j++) {
                GameObject lineObj = UIHelper.CreateUIObject("Line" + j, btnObj.transform);
                RectTransform lineRt = lineObj.GetComponent<RectTransform>();
                UIHelper.SetAnchors(lineRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
                lineRt.sizeDelta = new Vector2(36, 6);
                lineRt.anchoredPosition = new Vector2(0, 12 - (j * 12));
                UnityEngine.UI.Image lineImg = UIHelper.AddImage(lineObj, new Color32(220, 220, 220, 255));
                lineImg.sprite = UIHelper.CreateRoundedRectSprite(4, 1, Color.white, Color.white);
                lineImg.type = UnityEngine.UI.Image.Type.Sliced;
            }'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Replaced Gear Icon with Hamburger Icon!")
else:
    print("Failed to match Gear Icon!")
