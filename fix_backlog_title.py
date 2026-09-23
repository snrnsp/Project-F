import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any AddText call on titleObj in the backlog building section
# Wait, let's just find the exact corrupted string and replace it
# The exact string is probably "대화 로그" but corrupted. We can search for the line.
text = re.sub(r'UIHelper\.AddText\(titleObj,\s*".*?",\s*HalloweenTheme\.AccentOrange,\s*28,\s*TextAlignmentOptions\.Center\);',
              r'UIHelper.AddText(titleObj, "\\uB300\\uD654 \\uB85C\\uADF8", HalloweenTheme.AccentOrange, 28, TextAlignmentOptions.Center);', text)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed corrupted Backlog Title text')
