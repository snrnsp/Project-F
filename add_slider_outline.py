import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = """            // Background
            GameObject bgObj = UIHelper.CreateUIObject("Background", sliderObj.transform);
            UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
            Image bgImg = UIHelper.AddImage(bgObj, HalloweenTheme.SlotEmpty);"""

target_win = target.replace('\n', '\r\n')

replacement = """            // Background
            GameObject bgObj = UIHelper.CreateUIObject("Background", sliderObj.transform);
            UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
            Image bgImg = UIHelper.AddImage(bgObj, HalloweenTheme.SlotEmpty);
            
            UnityEngine.UI.Outline outline = bgObj.AddComponent<UnityEngine.UI.Outline>();
            outline.effectColor = HalloweenTheme.PanelBorder;
            outline.effectDistance = new Vector2(2f, 2f);"""
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Outline added (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Outline added (lf)')
else:
    print('Target not found')
