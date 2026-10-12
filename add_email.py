import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '// Text versionText = CreateLegacyText(verObj, "v1.0.0", new Color32(200, 200, 200, 200), 16, TextAnchor.LowerLeft);' in line:
        # Re-enable the block and change it to email
        lines[i-4] = '            GameObject verObj = UIHelper.CreateUIObject("ContactText", lobbyPanelRoot.transform);\n'
        lines[i-3] = '            RectTransform verRt = verObj.GetComponent<RectTransform>();\n'
        lines[i-2] = '            UIHelper.SetAnchors(verRt, new Vector2(0, 0), new Vector2(0, 0), new Vector2(0, 0));\n'
        lines[i-1] = '            verRt.anchoredPosition = new Vector2(20, 20);\n'
        lines[i] = '            Text contactText = CreateLegacyText(verObj, "loststudio.lost@gmail.com", new Color32(200, 200, 200, 200), 16, TextAnchor.LowerLeft);\n'
        break

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Added email to bottom left.")
