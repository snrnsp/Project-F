import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

new_layout = '''
            // --- Title Container (Horizontal Layout for perfect centering) ---
            GameObject titleContainer = new GameObject("TitleContainer");
            titleContainer.transform.SetParent(panel.transform, false);
            RectTransform contRt = titleContainer.AddComponent<RectTransform>();
            contRt.anchorMin = new Vector2(0, 1);
            contRt.anchorMax = new Vector2(1, 1);
            contRt.anchoredPosition = new Vector2(0, titleY);
            contRt.sizeDelta = new Vector2(0, 50);

            UnityEngine.UI.HorizontalLayoutGroup hlg = titleContainer.AddComponent<UnityEngine.UI.HorizontalLayoutGroup>();
            hlg.childAlignment = TextAnchor.MiddleCenter;
            hlg.spacing = 15;
            hlg.childControlWidth = false;
            hlg.childControlHeight = false;
            hlg.childForceExpandWidth = false;
            hlg.childForceExpandHeight = false;

            // Warning triangle
            GameObject triObj = new GameObject("WarningTriangle");
            triObj.transform.SetParent(titleContainer.transform, false);
            RectTransform triRt = triObj.AddComponent<RectTransform>();
            triRt.sizeDelta = new Vector2(triW, triH);
            Image triImg = triObj.AddComponent<Image>();
            triImg.sprite = triSprite;
            triImg.color = new Color32(255, 180, 50, 255);
            triImg.raycastTarget = false;

            // Title text
            GameObject iconObj = new GameObject("WarningTitle");
            iconObj.transform.SetParent(titleContainer.transform, false);
            RectTransform iconRt = iconObj.AddComponent<RectTransform>();
            TextMeshProUGUI iconText = Theme.UIHelper.AddText(iconObj, "\uAD11\uACFC\uBBFC\uC131 \uBC1C\uC791 \uACBD\uACE0", new Color32(255, 180, 80, 255), 30, TextAlignmentOptions.Center);
            iconText.fontStyle = FontStyles.Bold;
            UnityEngine.UI.ContentSizeFitter iconFitter = iconObj.AddComponent<UnityEngine.UI.ContentSizeFitter>();
            iconFitter.horizontalFit = UnityEngine.UI.ContentSizeFitter.FitMode.PreferredSize;
            iconFitter.verticalFit = UnityEngine.UI.ContentSizeFitter.FitMode.PreferredSize;

            // Warning message
            string warn = "<color=#FFD080>";
            string warnEnd = "</color>";
            GameObject msgObj = new GameObject("WarningMessage");
            msgObj.transform.SetParent(panel.transform, false);
            RectTransform msgRt = msgObj.AddComponent<RectTransform>();
            msgRt.anchorMin = new Vector2(0, 0.15f);
            msgRt.anchorMax = new Vector2(1, 0.80f);
            msgRt.offsetMin = new Vector2(60, 0);
            msgRt.offsetMax = new Vector2(-60, 0);
            TextMeshProUGUI msgText = Theme.UIHelper.AddText(msgObj,
                "\uADF9\uC18C\uC218\uC758 \uC0AC\uB78C\uB4E4\uC740 \uBE44\uB514\uC624 \uAC8C\uC784\uC5D0 \uB4F1\uC7A5\uD558\uB294 " +
                $"<b>{warn}\uBC88\uCA4D\uC774\uB294 \uBE5B{warnEnd}</b>\uC774\uB098 " +
                $"<b>{warn}\uD2B9\uC815 \uD328\uD134{warnEnd}</b>\uACFC \uAC19\uC740 \uC2DC\uAC01\uC801 \uC774\uBBF8\uC9C0\uC5D0 \uB178\uCD9C\uB420 \uB54C " +
                $"<b>{warn}\uAD11\uACFC\uBBFC\uC131 \uBC1C\uC791{warnEnd}</b>\uC744 \uC77C\uC73C\uD0AC \uC218 \uC788\uC2B5\uB2C8\uB2E4.\n\n" +
                "\uACFC\uAC70\uC5D0 \uBC1C\uC791 \uBCD1\uB825\uC774 \uC5C6\uC5C8\uB354\uB77C\uB3C4 \uAC8C\uC784\uC744 \uD558\uB294 \uB3D9\uC548 " +
                "\uC774\uB7EC\uD55C \uC99D\uC0C1\uC744 \uC720\uBC1C\uD560 \uC218 \uC788\uB294 \uBBF8\uD655\uC778 \uC0C1\uD0DC\uC77C \uC218 \uC788\uC2B5\uB2C8\uB2E4.\n\n" +
                $"\uAC8C\uC784 \uC911 <b>{warn}\uD604\uAE30\uC99D{warnEnd}</b>, <b>{warn}\uC2DC\uB825 \uC774\uC0C1{warnEnd}</b>, " +
                $"<b>{warn}\uB208\uC774\uB098 \uC5BC\uAD74\uC758 \uACBD\uB828{warnEnd}</b>, " +
                $"<b>{warn}\uD314\uB2E4\uB9AC\uC758 \uB5A8\uB9BC{warnEnd}</b>, <b>{warn}\uBC29\uD5A5 \uAC10\uAC01 \uC0C1\uC2E4{warnEnd}</b>, " +
                $"<b>{warn}\uD63C\uB780{warnEnd}</b>, " +
                $"\uB610\uB294 <b>{warn}\uC77C\uC2DC\uC801\uC778 \uC758\uC2DD \uC0C1\uC2E4{warnEnd}</b> \uB4F1\uC758 \uC99D\uC0C1\uC744 \uACA2\uB294\uB2E4\uBA74 " +
                $"<b>{warn}\uC989\uC2DC \uAC8C\uC784\uC744 \uC911\uB2E8{warnEnd}</b>\uD558\uACE0 \uC758\uC0AC\uC640 \uC0C1\uB2F4\uD558\uC2ED\uC2DC\uC624.",
                new Color32(200, 195, 210, 255), 21, TextAlignmentOptions.Center);
            msgText.lineSpacing = 20f;
            msgText.alignment = TextAlignmentOptions.CenterGeo;
'''

pattern = r'// Warning triangle\s*GameObject triObj = new GameObject\("WarningTriangle"\);.*?(?=\s*// Continue button)'
text = re.sub(pattern, new_layout.strip() + '\n\n', text, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated LobbyUI warning layout')
