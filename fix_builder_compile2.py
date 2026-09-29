import sys
import re

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# I will replace exactly the lines that need to be replaced by finding the index
start_idx = content.find('// ─── 2. Auto-play Delay ───')
end_idx = content.find('Slider autoPlaySlider = CreateSettingsSlider(panel.transform, yPos - 45);', start_idx) + len('Slider autoPlaySlider = CreateSettingsSlider(panel.transform, yPos - 45);')

new_logic = """// ─── 2. Auto-play Delay ───
        yPos -= 95;
        var autoPlayLabel = CreateSettingsLabel(panel.transform, "\\uC624\\uD1A0 \\uB300\\uAE30 \\uC2DC\\uAC04", yPos);
        Slider autoPlaySlider = CreateSettingsSlider(panel.transform, yPos - 45);

        // Value InputField (right side of slider)
        GameObject autoValObj = UIHelper.CreateUIObject("AutoPlayValue", panel.transform);
        RectTransform autoValRt = autoValObj.GetComponent<RectTransform>();
        UIHelper.SetAnchors(autoValRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
        autoValRt.anchoredPosition = new Vector2(235, yPos - 45); // slider spans -175 to 175. Center is 235
        autoValRt.sizeDelta = new Vector2(90, 30);

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
        Text autoPlayValueText = CreateLegacyText(inputTextObj, "2.0", HalloweenTheme.AccentOrange, 22, TextAnchor.MiddleCenter);
        autoPlayInputField.textComponent = autoPlayValueText;"""

content = content[:start_idx] + new_logic + content[end_idx:]

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("HalloweenUIBuilder updated properly without regex")
