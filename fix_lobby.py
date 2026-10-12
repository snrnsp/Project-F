import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'Image bgImg = UIHelper\.AddImage\(bgObj, new Color\(0\.72f, 0\.72f, 0\.72f, 1f\), bgSprite\); // Darkened background'

replacement = r'''Image bgImg = UIHelper.AddImage(bgObj, new Color(0.72f, 0.72f, 0.72f, 1f), bgSprite); // Darkened background
            UnityEngine.UI.AspectRatioFitter bgArf = bgObj.AddComponent<UnityEngine.UI.AspectRatioFitter>();
            bgArf.aspectMode = UnityEngine.UI.AspectRatioFitter.AspectMode.EnvelopeParent;
            bgArf.aspectRatio = 1920f / 1080f;'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed Lobby Background AspectRatioFitter!")
else:
    print("Failed to match Lobby background!")
