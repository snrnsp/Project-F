import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            // ===== Close Button =====
            GameObject closeBtnObj = UIHelper.CreateUIObject("CloseBtn", headerObj.transform);
            RectTransform closeRt = closeBtnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(1, 0.5f), new Vector2(1, 0.5f), new Vector2(1, 0.5f));
            closeRt.anchoredPosition = new Vector2(-40, 0);
            closeRt.sizeDelta = new Vector2(40, 40);
            UIHelper.AddImage(closeBtnObj, new Color32(180, 50, 50, 255));
            Button closeBtn = closeBtnObj.AddComponent<Button>();

            GameObject closeTextObj = UIHelper.CreateUIObject("Text", closeBtnObj.transform);
            UIHelper.StretchFull(closeTextObj.GetComponent<RectTransform>());
            UIHelper.AddText(closeTextObj, "X", Color.white, 24, TextAlignmentOptions.Center);'''

replacement = '''            // ===== Close Button =====
            GameObject closeBtnObj = UIHelper.CreateUIObject("CloseBtn", headerObj.transform);
            RectTransform closeRt = closeBtnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(closeRt, new Vector2(1, 0.5f), new Vector2(1, 0.5f), new Vector2(1, 0.5f));
            closeRt.anchoredPosition = new Vector2(-40, 0);
            closeRt.sizeDelta = new Vector2(40, 40);
            Image closeBtnImg = UIHelper.AddImage(closeBtnObj, Color.white);
            closeBtnImg.sprite = UIHelper.CreateRoundedRectSprite(8, 2, new Color32(180, 50, 50, 255), new Color32(255, 120, 120, 255));
            closeBtnImg.type = Image.Type.Sliced;
            Button closeBtn = closeBtnObj.AddComponent<Button>();

            GameObject closeTextObj = UIHelper.CreateUIObject("Text", closeBtnObj.transform);
            RectTransform textRt = closeTextObj.GetComponent<RectTransform>();
            UIHelper.StretchFull(textRt);
            // Nudge 'X' slightly up to perfectly center it visually against font baselines
            textRt.offsetMin = new Vector2(0, 2);
            textRt.offsetMax = new Vector2(0, 2);
            UIHelper.AddText(closeTextObj, "X", Color.white, 24, TextAlignmentOptions.Center);'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated close button style in CreateExtraUI')
else:
    print('Target not found')
