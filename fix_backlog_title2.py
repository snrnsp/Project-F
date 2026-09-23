import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'UIHelper\.AddText\(titleObj,\s*".*?",\s*HalloweenTheme\.AccentOrange,.*?\);',
              r'UIHelper.AddText(titleObj, "\\uB300\\uD654 \\uB85C\\uADF8", HalloweenTheme.AccentOrange, 28, TextAlignmentOptions.Center);', text)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

