import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# For SettingsUI
target_settings_bg = '''            GameObject settingsRoot = UIHelper.CreateUIObject("SettingsRoot", mainCanvas.transform);
            UIHelper.StretchFull(settingsRoot.GetComponent<RectTransform>());

            // Semi-transparent dark overlay
            UIHelper.AddImage(settingsRoot, new Color(0, 0, 0, 0.7f));'''

replacement_settings_bg = '''            GameObject settingsRoot = UIHelper.CreateUIObject("SettingsRoot", mainCanvas.transform);
            UIHelper.StretchFull(settingsRoot.GetComponent<RectTransform>());

            // Semi-transparent dark overlay (now a button to close)
            GameObject bgBtnObj = UIHelper.CreateUIObject("BackgroundButton", settingsRoot.transform);
            UIHelper.StretchFull(bgBtnObj.GetComponent<RectTransform>());
            UIHelper.AddImage(bgBtnObj, new Color(0, 0, 0, 0.7f));
            UnityEngine.UI.Button bgBtn = bgBtnObj.AddComponent<UnityEngine.UI.Button>();
            bgBtn.transition = UnityEngine.UI.Selectable.Transition.None;'''

text = text.replace(target_settings_bg, replacement_settings_bg)

target_settings_attach = '''            // Attach SettingsUI
            SettingsUI settingsUi = settingsRoot.AddComponent<SettingsUI>();
            settingsUiRef = settingsUi;'''

replacement_settings_attach = '''            // Attach SettingsUI
            SettingsUI settingsUi = settingsRoot.AddComponent<SettingsUI>();
            settingsUiRef = settingsUi;
            bgBtn.onClick.AddListener(() => settingsUi.Hide());'''

text = text.replace(target_settings_attach, replacement_settings_attach)

# For ExtraUI
target_extra_bg = '''            GameObject extraRoot = UIHelper.CreateUIObject("ExtraPanel", mainCanvas.transform);
            UIHelper.StretchFull(extraRoot.GetComponent<RectTransform>());
            extraRoot.SetActive(false);

            // Dark background
            Image bgImg = UIHelper.AddImage(extraRoot, new Color32(15, 8, 25, 255));'''

replacement_extra_bg = '''            GameObject extraRoot = UIHelper.CreateUIObject("ExtraPanel", mainCanvas.transform);
            UIHelper.StretchFull(extraRoot.GetComponent<RectTransform>());
            extraRoot.SetActive(false);

            // Dark background (now a button to close)
            GameObject extraBgBtnObj = UIHelper.CreateUIObject("BackgroundButton", extraRoot.transform);
            UIHelper.StretchFull(extraBgBtnObj.GetComponent<RectTransform>());
            Image bgImg = UIHelper.AddImage(extraBgBtnObj, new Color32(15, 8, 25, 200)); # Made slightly transparent so lobby is visible behind
            UnityEngine.UI.Button extraBgBtn = extraBgBtnObj.AddComponent<UnityEngine.UI.Button>();
            extraBgBtn.transition = UnityEngine.UI.Selectable.Transition.None;'''

text = text.replace(target_extra_bg, replacement_extra_bg)

target_extra_attach = '''            // Add ExtraUI Component
            extraUiRef = extraRoot.AddComponent<ExtraUI>();'''

replacement_extra_attach = '''            // Add ExtraUI Component
            extraUiRef = extraRoot.AddComponent<ExtraUI>();
            extraBgBtn.onClick.AddListener(() => extraUiRef.Hide());'''

text = text.replace(target_extra_attach, replacement_extra_attach)


with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added background click-to-close functionality to Settings and Extra UIs')
