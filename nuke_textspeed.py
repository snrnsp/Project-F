import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Hide SkipHelpPanel initially
content = re.sub(
    r'GameObject skipHelpPanelObj = UIHelper\.CreateUIObject\("SkipHelpPanel", panel\.transform\);',
    'GameObject skipHelpPanelObj = UIHelper.CreateUIObject("SkipHelpPanel", panel.transform);\n            skipHelpPanelObj.SetActive(false);',
    content
)

# 2. Complete rewrite of Text Speed block using fully independent gameobjects
start_marker = "float yPos = -100;"
end_marker = "            // Preview Text & Background"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_block = '''float yPos = -100;

            // 〓〓〓 1. Text Speed 〓〓〓
            GameObject tsLabelObj = new GameObject("TextSpeedLabel_HACK");
            tsLabelObj.transform.SetParent(panel.transform, false);
            RectTransform tsLabelRt = tsLabelObj.AddComponent<RectTransform>();
            tsLabelRt.anchorMin = new Vector2(0.5f, 1f);
            tsLabelRt.anchorMax = new Vector2(0.5f, 1f);
            tsLabelRt.pivot = new Vector2(0.5f, 1f);
            tsLabelRt.anchoredPosition = new Vector2(-160, yPos);
            tsLabelRt.sizeDelta = new Vector2(280, 40);
            Text textSpeedLabel = CreateLegacyText(tsLabelObj, Loc.Get("ui.settings.text_speed", "텍스트 속도 조절"), HalloweenTheme.TextPrimary, 24, TextAnchor.MiddleRight);

            GameObject tsSliderObj = new GameObject("TextSpeedSlider_HACK");
            tsSliderObj.transform.SetParent(panel.transform, false);
            RectTransform tsSliderRt = tsSliderObj.AddComponent<RectTransform>();
            tsSliderRt.anchorMin = new Vector2(0.5f, 1f);
            tsSliderRt.anchorMax = new Vector2(0.5f, 1f);
            tsSliderRt.pivot = new Vector2(0.5f, 1f);
            tsSliderRt.anchoredPosition = new Vector2(100, yPos);
            tsSliderRt.sizeDelta = new Vector2(240, 20);
            
            // Border
            GameObject borderObj = new GameObject("Border");
            borderObj.transform.SetParent(tsSliderObj.transform, false);
            RectTransform borderRt = borderObj.AddComponent<RectTransform>();
            borderRt.anchorMin = Vector2.zero; borderRt.anchorMax = Vector2.one;
            borderRt.offsetMin = new Vector2(-4, -4); borderRt.offsetMax = new Vector2(4, 4);
            UIHelper.AddImage(borderObj, new Color32(0, 0, 0, 255));
            
            // BG
            GameObject bgObj = new GameObject("Background");
            bgObj.transform.SetParent(tsSliderObj.transform, false);
            RectTransform bgRt = bgObj.AddComponent<RectTransform>();
            bgRt.anchorMin = Vector2.zero; bgRt.anchorMax = Vector2.one;
            bgRt.offsetMin = Vector2.zero; bgRt.offsetMax = Vector2.zero;
            UIHelper.AddImage(bgObj, new Color32(100, 80, 130, 255));
            
            // Fill Area
            GameObject fillAreaObj = new GameObject("Fill Area");
            fillAreaObj.transform.SetParent(tsSliderObj.transform, false);
            RectTransform fillAreaRt = fillAreaObj.AddComponent<RectTransform>();
            fillAreaRt.anchorMin = Vector2.zero; fillAreaRt.anchorMax = Vector2.one;
            fillAreaRt.offsetMin = new Vector2(4, 0); fillAreaRt.offsetMax = new Vector2(-4, 0);
            
            // Fill
            GameObject fillObj = new GameObject("Fill");
            fillObj.transform.SetParent(fillAreaObj.transform, false);
            RectTransform fillRt = fillObj.AddComponent<RectTransform>();
            fillRt.anchorMin = Vector2.zero; fillRt.anchorMax = Vector2.one;
            fillRt.offsetMin = Vector2.zero; fillRt.offsetMax = Vector2.zero;
            UIHelper.AddImage(fillObj, HalloweenTheme.AccentOrange);
            
            Slider textSpeedSlider = tsSliderObj.AddComponent<Slider>();
            textSpeedSlider.transition = Selectable.Transition.None;
            textSpeedSlider.fillRect = fillRt;

'''
    content = content[:start_idx] + new_block + content[end_idx:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Rewrote text speed block entirely.")
