import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            // Button styling
            Image btnImg = UIHelper.AddImage(btnObj, new Color32(30, 20, 40, 200));
            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            btn.colors = HalloweenTheme.GetButtonColors();
            btn.onClick.AddListener(() => globalMgr.ToggleSettings());
            
            UnityEngine.UI.Outline outline = btnObj.AddComponent<UnityEngine.UI.Outline>();
            outline.effectColor = HalloweenTheme.PanelBorder;
            outline.effectDistance = new Vector2(4, 4);

            // Gear Icon
            GameObject iconObj = UIHelper.CreateUIObject("Icon", btnObj.transform);
            UIHelper.StretchFull(iconObj.GetComponent<RectTransform>());
            Text iconText = iconObj.AddComponent<Text>();
            iconText.text = "\u2699"; // Gear emoji
            iconText.alignment = TextAnchor.MiddleCenter;
            iconText.alignByGeometry = true;
            iconText.fontSize = 40;
            iconText.color = Color.white;
            iconText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");'''

replacement = '''            // Button styling (Invisible hit box)
            Image btnImg = UIHelper.AddImage(btnObj, new Color(0, 0, 0, 0));
            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            btn.colors = HalloweenTheme.GetButtonColors();
            btn.onClick.AddListener(() => globalMgr.ToggleSettings());

            // Gear Icon
            GameObject iconObj = UIHelper.CreateUIObject("Icon", btnObj.transform);
            UIHelper.StretchFull(iconObj.GetComponent<RectTransform>());
            Text iconText = iconObj.AddComponent<Text>();
            iconText.text = "\u2699"; // Gear emoji
            iconText.alignment = TextAnchor.MiddleCenter;
            iconText.alignByGeometry = true;
            iconText.fontSize = 40;
            iconText.color = Color.white;
            
            // Link text as target graphic so the gear itself reacts to hover/click!
            btn.targetGraphic = iconText;
            
            // Assign font
            string[] fontNames = { 
                "Malgun Gothic", "Apple SD Gothic Neo",
                "Meiryo", "Yu Gothic", "MS Gothic", "Hiragino Sans",
                "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC",
                "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC",
                "Arial Unicode MS", "sans-serif"
            };
            Font rawFont = Font.CreateDynamicFontFromOSFont(fontNames, 40);
            if (rawFont != null) iconText.font = rawFont;
            else iconText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated GlobalSettingsBtn to be text-only')
