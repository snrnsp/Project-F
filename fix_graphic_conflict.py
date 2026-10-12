import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

bad_line = 'Text autoPlayValueText = CreateLegacyText(inputTextObj, "2.0", new Color32(255, 255, 255, 255), 20, TextAnchor.MiddleCenter);'
good_lines = '''GameObject textChildObj = UIHelper.CreateUIObject("Text", inputTextObj.transform);
            UIHelper.StretchFull(textChildObj.GetComponent<RectTransform>());
            Text autoPlayValueText = CreateLegacyText(textChildObj, "2.0", new Color32(255, 255, 255, 255), 20, TextAnchor.MiddleCenter);'''

content = content.replace(bad_line, good_lines)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed Text component on Image bug!")
