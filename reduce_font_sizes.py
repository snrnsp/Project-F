import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target1 = 'TextMeshProUGUI nameText = UIHelper.AddText(nameObj, "", Color.black, 60, TextAlignmentOptions.Left);'
replacement1 = 'TextMeshProUGUI nameText = UIHelper.AddText(nameObj, "", Color.black, 55, TextAlignmentOptions.Left);'

target2 = 'TextMeshProUGUI profileText = UIHelper.AddText(profileObj, "", Color.black, 36, TextAlignmentOptions.TopLeft);'
replacement2 = 'TextMeshProUGUI profileText = UIHelper.AddText(profileObj, "", Color.black, 32, TextAlignmentOptions.TopLeft);'

text = text.replace(target1, replacement1)
text = text.replace(target2, replacement2)

with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated font sizes')
