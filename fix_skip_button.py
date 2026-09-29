import sys

with open('Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

target = '''            var autoTuple = CreateLegacyButton(dialoguePanel.transform, "AUTO", btnW, btnH, new Color32(40, 25, 60, 255), softIndigo, true);
            RectTransform autoRt = autoTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(autoRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            // pivot is 1, 1. Placed above the panel (Y=56) to sit on top of the 6px outline.
            autoRt.anchoredPosition = new Vector2(-(10 + btnW + btnSpacing), 56);
            Text autoText = autoTuple.text;
            autoText.fontSize = 32;



            var logTuple = CreateLegacyButton(dialoguePanel.transform, "LOG", btnW, btnH, new Color32(40, 25, 60, 255), softIndigo, true);'''

replacement = '''            var autoTuple = CreateLegacyButton(dialoguePanel.transform, "AUTO", btnW, btnH, new Color32(40, 25, 60, 255), softIndigo, true);
            RectTransform autoRt = autoTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(autoRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            // pivot is 1, 1. Placed above the panel (Y=56) to sit on top of the 6px outline.
            autoRt.anchoredPosition = new Vector2(-(10 + 2 * btnW + 2 * btnSpacing), 56);
            Text autoText = autoTuple.text;
            autoText.fontSize = 32;

            var inGameSkipTuple = CreateLegacyButton(dialoguePanel.transform, "SKIP", btnW, btnH, new Color32(40, 25, 60, 255), softIndigo, true);
            RectTransform inGameSkipRt = inGameSkipTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(inGameSkipRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            inGameSkipRt.anchoredPosition = new Vector2(-(10 + btnW + btnSpacing), 56);
            Text inGameSkipText = inGameSkipTuple.text;
            inGameSkipText.fontSize = 32;

            var logTuple = CreateLegacyButton(dialoguePanel.transform, "LOG", btnW, btnH, new Color32(40, 25, 60, 255), softIndigo, true);'''

if target in content:
    content = content.replace(target, replacement)
    print('Target 1 replaced')
else:
    print('Target 1 not found')

target2 = '''            UIHelper.SetField(ui, "autoButton", autoTuple.btn);
            UIHelper.SetField(ui, "backlogButton", logTuple.btn);'''

replacement2 = '''            UIHelper.SetField(ui, "autoButton", autoTuple.btn);
            UIHelper.SetField(ui, "skipButton", inGameSkipTuple.btn);
            UIHelper.SetField(ui, "backlogButton", logTuple.btn);'''

if target2 in content:
    content = content.replace(target2, replacement2)
    print('Target 2 replaced')
else:
    print('Target 2 not found')

with open('Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)

