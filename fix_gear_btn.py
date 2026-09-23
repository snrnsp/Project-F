import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            Image btnImg = UIHelper.AddImage(btnObj, new Color(0, 0, 0, 0));
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
            btn.targetGraphic = iconText;'''

replacement = '''            Image btnImg = UIHelper.AddImage(btnObj, new Color(0, 0, 0, 0));
            Button btn = btnObj.AddComponent<Button>();
            btn.transition = Selectable.Transition.ColorTint;
            
            ColorBlock cb = ColorBlock.defaultColorBlock;
            cb.normalColor = Color.white;
            cb.highlightedColor = new Color32(200, 200, 200, 255); // Slightly gray on hover
            cb.pressedColor = new Color32(150, 150, 150, 255);     // Darker gray on click
            cb.selectedColor = Color.white;
            cb.colorMultiplier = 1f;
            cb.fadeDuration = 0.15f;
            btn.colors = cb;
            
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
            
            // Add black outline to the gear text
            UnityEngine.UI.Outline textOutline = iconObj.AddComponent<UnityEngine.UI.Outline>();
            textOutline.effectColor = new Color(0, 0, 0, 1);
            textOutline.effectDistance = new Vector2(2, -2);
            
            // Link text as target graphic so the gear itself reacts to hover/click!
            btn.targetGraphic = iconText;'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated gear icon to white with black outline and gray hover')
else:
    print('Target not found')
