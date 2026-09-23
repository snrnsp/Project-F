import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = 'var autoBtnTuple = UIHelper.CreateButton(dialoguePanel.transform, "AUTO", btnW, btnH);'
rep1 = 'var autoBtnTuple = CreateLegacyButton(dialoguePanel.transform, "AUTO", btnW, btnH, new Color32(40, 25, 60, 255));'

target2 = 'var skipBtnTuple = UIHelper.CreateButton(dialoguePanel.transform, "SKIP", btnW, btnH);'
rep2 = 'var skipBtnTuple = CreateLegacyButton(dialoguePanel.transform, "SKIP", btnW, btnH, new Color32(40, 25, 60, 255));'

target3 = 'var backlogBtnTuple = UIHelper.CreateButton(dialoguePanel.transform, "LOG", btnW, btnH);'
rep3 = 'var backlogBtnTuple = CreateLegacyButton(dialoguePanel.transform, "LOG", btnW, btnH, new Color32(40, 25, 60, 255));'

text = text.replace(target1, rep1).replace(target2, rep2).replace(target3, rep3)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated Dialogue UI buttons to use LegacyText')
