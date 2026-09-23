import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            // Delete Data Button
            var deleteTuple = CreateLegacyButton(panel.transform, "데이터 삭제", 200, 50, new Color32(180, 40, 40, 255));
            RectTransform deleteRt = deleteTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(deleteRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            deleteRt.anchoredPosition = new Vector2(-120, 40);'''

replacement = '''            // Delete Data Button
            var deleteTuple = CreateLegacyButton(panel.transform, "데이터 삭제", 200, 50, new Color32(180, 40, 40, 255));
            
            // Custom button color behavior for Delete Button
            UnityEngine.UI.ColorBlock delCb = deleteTuple.btn.colors;
            delCb.normalColor = new Color32(180, 40, 40, 255);       // Red normal
            delCb.highlightedColor = new Color32(180, 40, 40, 255);  // No hover reaction
            delCb.selectedColor = new Color32(180, 40, 40, 255);     // No focus reaction
            delCb.pressedColor = new Color32(120, 10, 10, 255);      // Deep red when pressed
            deleteTuple.btn.colors = delCb;

            RectTransform deleteRt = deleteTuple.btn.GetComponent<RectTransform>();
            UIHelper.SetAnchors(deleteRt, new Vector2(0.5f, 0), new Vector2(0.5f, 0), new Vector2(0.5f, 0));
            deleteRt.anchoredPosition = new Vector2(-120, 40);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated Delete Data button colors successfully')
else:
    print('Target not found')
