import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = """            // Delete Data Button
            var deleteTuple = CreateLegacyButton(panel.transform, "데이터 삭제", 200, 50, new Color32(180, 40, 40, 255));

            // Custom button color behavior for Delete Button
            UnityEngine.UI.ColorBlock delCb = deleteTuple.btn.colors;
            delCb.normalColor = new Color32(180, 40, 40, 255);       // Red normal
            delCb.highlightedColor = new Color32(180, 40, 40, 255);  // No hover reaction
            delCb.selectedColor = new Color32(180, 40, 40, 255);     // No focus reaction
            delCb.pressedColor = new Color32(120, 10, 10, 255);      // Deep red when pressed
            deleteTuple.btn.colors = delCb;

            // Remove hover script to ensure absolutely zero hover reaction
            Component hoverScript = deleteTuple.btn.GetComponent("LobbyButtonHover");
            if (hoverScript != null) UnityEngine.Object.Destroy(hoverScript);

            RectTransform deleteRt = deleteTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(deleteRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            deleteRt.anchoredPosition = new Vector2(-120, 40);

            // Close Button
            var closeTuple = CreateLegacyButton(panel.transform, "닫기", 200, 50, HalloweenTheme.ButtonNormal);
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(120, 40);"""

target_win = target.replace('\n', '\r\n')
replacement = """            // Close Button
            var closeTuple = CreateLegacyButton(panel.transform, "닫기", 200, 50, HalloweenTheme.ButtonNormal);
            RectTransform closeRt = closeTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            closeRt.anchoredPosition = new Vector2(0, 40);"""
replacement_win = replacement.replace('\n', '\r\n')

if target_win in text:
    text = text.replace(target_win, replacement_win)
    with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Replaced successfully (win lf)')
elif target in text:
    text = text.replace(target, replacement)
    with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Replaced successfully (lf)')
else:
    print('Target not found')
