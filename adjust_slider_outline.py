import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = """            UnityEngine.UI.Outline outline = bgObj.AddComponent<UnityEngine.UI.Outline>();
            outline.effectColor = HalloweenTheme.PanelBorder;
            outline.effectDistance = new Vector2(2f, 2f);"""
target_win = target.replace('\n', '\r\n')

replacement = """            UnityEngine.UI.Outline outline = bgObj.AddComponent<UnityEngine.UI.Outline>();
            outline.effectColor = HalloweenTheme.BackgroundDark;
            outline.effectDistance = new Vector2(4f, 4f);"""
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Outline adjusted (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Outline adjusted (lf)')
else:
    print('Target not found')
