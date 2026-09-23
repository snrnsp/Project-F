import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = 'private GlobalUIManager globalMgrRef;'
replacement1 = '''private GlobalUIManager globalMgrRef;
        private GameObject globalSettingsBtnObj;'''

target2 = '''            // Settings Button (Top Right)
            GameObject btnObj = UIHelper.CreateUIObject("GlobalSettingsBtn", globalRoot.transform);'''
replacement2 = '''            // Settings Button (Top Right)
            GameObject btnObj = UIHelper.CreateUIObject("GlobalSettingsBtn", globalRoot.transform);
            globalSettingsBtnObj = btnObj;'''

target3 = '''UIHelper.SetField(extraUi, "extraPanel", panel);'''
replacement3 = '''UIHelper.SetField(extraUi, "extraPanel", panel);
            UIHelper.SetField(extraUi, "globalSettingsButton", globalSettingsBtnObj);'''

text = text.replace(target1, replacement1).replace(target2, replacement2).replace(target3, replacement3)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated HalloweenUIBuilder.cs to wire globalSettingsButton to ExtraUI')
