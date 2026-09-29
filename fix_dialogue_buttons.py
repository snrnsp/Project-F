import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if '// Auto / Skip / Log Buttons (top-right of dialogue panel)' in line:
        new_lines.append('            // Auto / Skip / Log Buttons (moved to bottom-right of screen, above panel)\n')
        new_lines.append('            float btnW = 140, btnH = 50, btnSpacing = 10;\n')
        new_lines.append('\n')
        new_lines.append('            var autoTuple = CreateLegacyButton(dialoguePanelRoot.transform, "AUTO", btnW, btnH, new Color32(40, 25, 60, 255));\n')
        new_lines.append('            RectTransform autoRt = autoTuple.btn.GetComponent<RectTransform>();\n')
        new_lines.append('            UIHelper.SetAnchors(autoRt, new Vector2(1, 0), new Vector2(1, 0), new Vector2(1, 0));\n')
        new_lines.append('            autoRt.anchoredPosition = new Vector2(-(30 + btnW * 2 + btnSpacing * 2), 310);\n')
        new_lines.append('            Text autoText = autoTuple.text;\n')
        new_lines.append('            autoText.fontSize = 32;\n')
        new_lines.append('\n')
        new_lines.append('            var skipTuple = CreateLegacyButton(dialoguePanelRoot.transform, "SKIP", btnW, btnH, new Color32(40, 25, 60, 255));\n')
        new_lines.append('            RectTransform skipRt = skipTuple.btn.GetComponent<RectTransform>();\n')
        new_lines.append('            UIHelper.SetAnchors(skipRt, new Vector2(1, 0), new Vector2(1, 0), new Vector2(1, 0));\n')
        new_lines.append('            skipRt.anchoredPosition = new Vector2(-(30 + btnW + btnSpacing), 310);\n')
        new_lines.append('            skipTuple.text.fontSize = 32;\n')
        new_lines.append('\n')
        new_lines.append('            var logTuple = CreateLegacyButton(dialoguePanelRoot.transform, "LOG", btnW, btnH, new Color32(40, 25, 60, 255));\n')
        new_lines.append('            RectTransform logRt = logTuple.btn.GetComponent<RectTransform>();\n')
        new_lines.append('            UIHelper.SetAnchors(logRt, new Vector2(1, 0), new Vector2(1, 0), new Vector2(1, 0));\n')
        new_lines.append('            logRt.anchoredPosition = new Vector2(-30, 310);\n')
        new_lines.append('            logTuple.text.fontSize = 32;\n')
        skip = True
        continue
        
    if skip:
        if '// Attach DialogueUI and wire fields' in line:
            skip = False
            new_lines.append(line)
        continue
        
    if not skip:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(new_lines)
print("HalloweenUIBuilder updated to move dialogue buttons right and increase size")
