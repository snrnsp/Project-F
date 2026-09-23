import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Store lobbySettingsButton at class level
target1 = '''private GameObject globalSettingsBtnObj;'''
replacement1 = '''private GameObject globalSettingsBtnObj;
        private GameObject lobbySettingsBtnObj;'''

target2 = '''            var settingsTuple = CreateLegacyButton(lobbyPanelRoot.transform, "\ud658\uacbd \uc124\uc815", 260, 55, btnBg);'''
replacement2 = '''            var settingsTuple = CreateLegacyButton(lobbyPanelRoot.transform, "\ud658\uacbd \uc124\uc815", 260, 55, btnBg);
            lobbySettingsBtnObj = settingsTuple.btn.gameObject;'''

target3 = '''UIHelper.SetField(extraUi, "globalSettingsButton", globalSettingsBtnObj);'''
replacement3 = '''UIHelper.SetField(extraUi, "globalSettingsButton", globalSettingsBtnObj);
            UIHelper.SetField(extraUi, "lobbySettingsButton", lobbySettingsBtnObj);'''

if target1 in text and target2 in text and target3 in text:
    text = text.replace(target1, replacement1).replace(target2, replacement2).replace(target3, replacement3)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Wired lobbySettingsBtnObj to ExtraUI')
else:
    print('Targets not found')
