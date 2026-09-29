import sys
import re

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_logic = """// ─── 2. Auto-play Delay ───
        yPos -= 95;
        var autoPlayLabel = CreateSettingsLabel(panel.transform, "\\uC624\\uD1A0 \\uB300\\uAE30 \\uC2DC\\uAC04", yPos);
        // Value text (right-aligned)
        GameObject autoValObj = UIHelper.CreateUIObject("AutoPlayValue", panel.transform);
        RectTransform autoValRt = autoValObj.GetComponent<RectTransform>();
        UIHelper.SetAnchors(autoValRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
        autoValRt.anchoredPosition = new Vector2(130, yPos);
        autoValRt.sizeDelta = new Vector2(100, 35);
        Text autoPlayValueText = CreateLegacyText(autoValObj, "2.0", HalloweenTheme.AccentOrange, 26, TextAnchor.UpperRight);
        Slider autoPlaySlider = CreateSettingsSlider(panel.transform, yPos - 45);"""

new_logic = """// ─── 2. Auto-play Delay ───
        yPos -= 95;
        var autoPlayLabel = CreateSettingsLabel(panel.transform, "\\uC624\\uD1A0 \\uB300\\uAE30 \\uC2DC\\uAC04", yPos);
        Slider autoPlaySlider = CreateSettingsSlider(panel.transform, yPos - 45);

        // Value InputField (right side of slider)
        GameObject autoValObj = UIHelper.CreateUIObject("AutoPlayValue", panel.transform);
        RectTransform autoValRt = autoValObj.GetComponent<RectTransform>();
        UIHelper.SetAnchors(autoValRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
        autoValRt.anchoredPosition = new Vector2(235, yPos - 45); // slider is 350 wide (-175 to 175)
        autoValRt.sizeDelta = new Vector2(90, 40);

        UnityEngine.UI.Image inputBg = UIHelper.AddImage(autoValObj, new Color32(0, 0, 0, 150));
        UnityEngine.UI.Outline outline = autoValObj.AddComponent<UnityEngine.UI.Outline>();
        outline.effectColor = HalloweenTheme.AccentOrange;
        outline.effectDistance = new Vector2(2, -2);

        UnityEngine.UI.InputField autoPlayInputField = autoValObj.AddComponent<UnityEngine.UI.InputField>();
        autoPlayInputField.transition = UnityEngine.UI.Selectable.Transition.ColorTint;
        autoPlayInputField.characterValidation = UnityEngine.UI.InputField.CharacterValidation.Decimal;

        GameObject inputTextObj = UIHelper.CreateUIObject("Text", autoValObj.transform);
        RectTransform inputTextRt = inputTextObj.GetComponent<RectTransform>();
        UIHelper.StretchFull(inputTextRt);
        inputTextRt.offsetMin = new Vector2(0, 0);
        inputTextRt.offsetMax = new Vector2(0, 0);
        Text autoPlayValueText = CreateLegacyText(inputTextObj, "2.0", HalloweenTheme.AccentOrange, 24, TextAnchor.MiddleCenter);
        autoPlayInputField.textComponent = autoPlayValueText;"""

content = content.replace(old_logic, new_logic)
content = content.replace('UIHelper.SetField(settingsUi, "autoPlayValueText", autoPlayValueText);', 'UIHelper.SetField(settingsUi, "autoPlayInputField", autoPlayInputField);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("HalloweenUIBuilder updated for InputField")
