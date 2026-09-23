import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Title
text = text.replace('UIHelper.AddText(titleObj, "\\uB300\\uD654 \\uB85C\\uADF8", HalloweenTheme.AccentOrange, 28, TextAlignmentOptions.Center);', 'UIHelper.AddText(titleObj, "\\uc5b8\\uc5b4 \\uc124\\uc815", HalloweenTheme.AccentOrange, 28, TextAlignmentOptions.Center);')

# Fix background button for LanguageUI
target_lang_bg = '''            GameObject langRoot = UIHelper.CreateUIObject("LanguageRoot", mainCanvas.transform);
            UIHelper.StretchFull(langRoot.GetComponent<RectTransform>());

            // Semi-transparent dark overlay
            UIHelper.AddImage(langRoot, new Color(0, 0, 0, 0.7f));'''

replacement_lang_bg = '''            GameObject langRoot = UIHelper.CreateUIObject("LanguageRoot", mainCanvas.transform);
            UIHelper.StretchFull(langRoot.GetComponent<RectTransform>());

            // Semi-transparent dark overlay (now a button to close)
            GameObject langBgBtnObj = UIHelper.CreateUIObject("BackgroundButton", langRoot.transform);
            UIHelper.StretchFull(langBgBtnObj.GetComponent<RectTransform>());
            UIHelper.AddImage(langBgBtnObj, new Color(0, 0, 0, 0.7f));
            UnityEngine.UI.Button langBgBtn = langBgBtnObj.AddComponent<UnityEngine.UI.Button>();
            langBgBtn.transition = UnityEngine.UI.Selectable.Transition.None;'''

text = text.replace(target_lang_bg, replacement_lang_bg)

# Attach close to background button
target_lang_attach = '''            // Attach LanguageUI
            LanguageUI langUi = langRoot.AddComponent<LanguageUI>();'''

replacement_lang_attach = '''            // Attach LanguageUI
            LanguageUI langUi = langRoot.AddComponent<LanguageUI>();
            langBgBtn.onClick.AddListener(() => langUi.Hide());'''

text = text.replace(target_lang_attach, replacement_lang_attach)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed LanguageUI title and added background button')
