import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: skipHelpTextBtn
bad_line1 = 'Text skipHelpTextBtn = CreateLegacyText(skipHelpBtnObj, "?", HalloweenTheme.AccentOrange, 22, TextAnchor.MiddleCenter);'
good_lines1 = '''GameObject skipHelpTextBtnObj = UIHelper.CreateUIObject("Text", skipHelpBtnObj.transform);
            UIHelper.StretchFull(skipHelpTextBtnObj.GetComponent<RectTransform>());
            Text skipHelpTextBtn = CreateLegacyText(skipHelpTextBtnObj, "?", HalloweenTheme.AccentOrange, 22, TextAnchor.MiddleCenter);'''
content = content.replace(bad_line1, good_lines1)

# Fix 2: skipHelpPanelText
bad_line2 = 'Text skipHelpPanelText = CreateLegacyText(skipHelpPanelObj, Loc.Get("ui.settings.skip_desc", "설정하신 단축키를 누르고 있으면 대사를 빠르게 넘길 수 있습니다."), new Color32(200, 190, 210, 255), 18, TextAnchor.MiddleCenter);'
good_lines2 = '''GameObject skipHelpPanelTextObj = UIHelper.CreateUIObject("Text", skipHelpPanelObj.transform);
            UIHelper.StretchFull(skipHelpPanelTextObj.GetComponent<RectTransform>());
            Text skipHelpPanelText = CreateLegacyText(skipHelpPanelTextObj, Loc.Get("ui.settings.skip_desc", "설정하신 단축키를 누르고 있으면 대사를 빠르게 넘길 수 있습니다."), new Color32(200, 190, 210, 255), 18, TextAnchor.MiddleCenter);'''
content = content.replace(bad_line2, good_lines2)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed remaining Image vs Text graphic conflicts!")
