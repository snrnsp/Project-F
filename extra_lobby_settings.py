import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '[SerializeField] private GameObject globalSettingsButton;'
replacement1 = '''[SerializeField] private GameObject globalSettingsButton;
        [SerializeField] private GameObject lobbySettingsButton;'''

target2 = 'if (globalSettingsButton != null) globalSettingsButton.SetActive(false);'
replacement2 = '''if (globalSettingsButton != null) globalSettingsButton.SetActive(false);
            if (lobbySettingsButton != null) lobbySettingsButton.SetActive(false);'''

target3 = 'if (globalSettingsButton != null) globalSettingsButton.SetActive(true);'
replacement3 = '''if (globalSettingsButton != null) globalSettingsButton.SetActive(true);
            if (lobbySettingsButton != null) lobbySettingsButton.SetActive(true);'''

if target1 in text:
    text = text.replace(target1, replacement1).replace(target2, replacement2).replace(target3, replacement3)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated ExtraUI.cs to also hide lobbySettingsButton')
else:
    print('Target not found')
