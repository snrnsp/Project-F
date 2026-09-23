import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = 'var autoTuple = UIHelper.CreateButton(dialoguePanel.transform, "AUTO", btnW, btnH);'
rep1 = 'var autoTuple = CreateLegacyButton(dialoguePanel.transform, "AUTO", btnW, btnH, new Color32(40, 25, 60, 255));'

target1b = 'TextMeshProUGUI autoText = autoTuple.btn.GetComponentInChildren<TextMeshProUGUI>();'
rep1b = 'Text autoText = autoTuple.text;'

target2 = 'var skipTuple = UIHelper.CreateButton(dialoguePanel.transform, "SKIP", btnW, btnH);'
rep2 = 'var skipTuple = CreateLegacyButton(dialoguePanel.transform, "SKIP", btnW, btnH, new Color32(40, 25, 60, 255));'

target3 = 'var logTuple = UIHelper.CreateButton(dialoguePanel.transform, "LOG", btnW, btnH);'
rep3 = 'var logTuple = CreateLegacyButton(dialoguePanel.transform, "LOG", btnW, btnH, new Color32(40, 25, 60, 255));'

target4 = 'UIHelper.SetField(ui, "skipButtonText", skipTuple.Item2);'
rep4 = 'UIHelper.SetField(ui, "skipButtonText", skipTuple.text);'

target5 = 'UIHelper.SetField(ui, "backlogButtonText", logTuple.Item2);'
rep5 = 'UIHelper.SetField(ui, "backlogButtonText", logTuple.text);'

text = text.replace(target1, rep1).replace(target1b, rep1b).replace(target2, rep2).replace(target3, rep3)
text = text.replace(target4, rep4).replace(target5, rep5)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated Dialogue UI buttons to CreateLegacyButton successfully')
