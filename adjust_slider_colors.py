import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = """            // Background
            GameObject bgObj = UIHelper.CreateUIObject("Background", sliderObj.transform);
            UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
            Image bgImg = UIHelper.AddImage(bgObj, HalloweenTheme.SlotEmpty);
            
            UnityEngine.UI.Outline outline = bgObj.AddComponent<UnityEngine.UI.Outline>();
            outline.effectColor = HalloweenTheme.BackgroundDark;
            outline.effectDistance = new Vector2(4f, 4f);"""

target_win = target.replace('\n', '\r\n')

replacement = """            // Background
            GameObject bgObj = UIHelper.CreateUIObject("Background", sliderObj.transform);
            UIHelper.StretchFull(bgObj.GetComponent<RectTransform>());
            // Use a noticeably lighter purple for the slider background so it stands out
            Image bgImg = UIHelper.AddImage(bgObj, new Color32(100, 80, 130, 255));
            
            UnityEngine.UI.Outline outline = bgObj.AddComponent<UnityEngine.UI.Outline>();
            // Use pure black for the border to guarantee it is visible
            outline.effectColor = new Color32(0, 0, 0, 255);
            outline.effectDistance = new Vector2(4f, 4f);"""
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Slider bg and outline adjusted (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Slider bg and outline adjusted (lf)')
else:
    print('Target not found')
