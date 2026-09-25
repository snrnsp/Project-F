import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = """            // Settings panel
            GameObject panel = UIHelper.CreatePanel("SettingsPanel", settingsRoot.transform, HalloweenTheme.PanelBackground);
            RectTransform panelRt = panel.GetComponent<RectTransform>();
            UIHelper.SetAnchors(panelRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            panelRt.sizeDelta = new Vector2(700, 600);"""

target_win = target.replace('\n', '\r\n')

replacement = """            // Settings panel
            GameObject panel = UIHelper.CreatePanel("SettingsPanel", settingsRoot.transform, HalloweenTheme.PanelBackground);
            UnityEngine.UI.Outline outline = panel.GetComponent<UnityEngine.UI.Outline>();
            if (outline != null) outline.effectDistance = new Vector2(HalloweenTheme.PanelBorderWidth, HalloweenTheme.PanelBorderWidth + 4f);
            RectTransform panelRt = panel.GetComponent<RectTransform>();
            UIHelper.SetAnchors(panelRt, new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f), new Vector2(0.5f, 0.5f));
            panelRt.sizeDelta = new Vector2(700, 600);"""
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Outline distance adjusted (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Outline distance adjusted (lf)')
else:
    print('Target not found')
