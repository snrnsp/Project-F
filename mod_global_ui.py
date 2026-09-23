import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Insert method call
text = text.replace('CreateScreenTransition();', 'CreateGlobalUI();\n            CreateScreenTransition();')

# Insert method definition
method_def = '''
        private void CreateGlobalUI()
        {
            GameObject globalRoot = UIHelper.CreateUIObject("GlobalUI", mainCanvas.transform);
            UIHelper.StretchFull(globalRoot.GetComponent<RectTransform>());

            var globalMgr = globalRoot.AddComponent<GlobalUIManager>();
            
            // Find settings root
            var settingsUI = Object.FindObjectOfType<SettingsUI>(true);
            if (settingsUI != null) globalMgr.Initialize(settingsUI.gameObject);

            // Settings Button (Top Right)
            GameObject btnObj = UIHelper.CreateUIObject("GlobalSettingsBtn", globalRoot.transform);
            RectTransform btnRt = btnObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(btnRt, new Vector2(1, 1), new Vector2(1, 1), new Vector2(1, 1));
            btnRt.anchoredPosition = new Vector2(-20, -20);
            btnRt.sizeDelta = new Vector2(60, 60);

            // Button styling
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
            iconText.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
        }

        private void CreateScreenTransition()'''

text = text.replace('private void CreateScreenTransition()', method_def.strip())

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added GlobalUIManager and Settings button')
