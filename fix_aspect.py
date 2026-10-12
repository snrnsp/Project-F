import codecs
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

pattern = r'Image backgroundImage = UIHelper\.AddImage\(bgImgObj, new Color\(1,1,1,0\)\);'

replacement = r'''Image backgroundImage = UIHelper.AddImage(bgImgObj, new Color(1,1,1,0));
            UnityEngine.UI.AspectRatioFitter arf = bgImgObj.AddComponent<UnityEngine.UI.AspectRatioFitter>();
            arf.aspectMode = UnityEngine.UI.AspectRatioFitter.AspectMode.EnvelopeParent;
            arf.aspectRatio = 1920f / 1080f;'''

new_content = re.sub(pattern, replacement, content)

if content != new_content:
    with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)
    print("Fixed BackgroundImage AspectRatioFitter in DialogueUI!")
else:
    print("Failed to match pattern!")
