import re

with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    code = f.read()

pattern = re.compile(r'// \?\? Return to Title Button \?\?.*?titleBtnRt\.anchoredPosition = new Vector2\(0, 50\);', re.DOTALL)
replacement = '''// ?? Return to Title Button ??
            yPos -= 105;
            var titleTuple = CreateLegacyButton(panel.transform, Loc.Get("ui.settings.return_to_title", "타이틀로 돌아가기"), 220, 44, new Color32(180, 50, 50, 255));
            RectTransform titleBtnRt = titleTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(titleBtnRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            titleBtnRt.anchoredPosition = new Vector2(0, yPos - 45);'''

code = re.sub(pattern, replacement, code)

with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
    f.write(code)
