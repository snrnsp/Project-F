import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Declare a field
text = text.replace('private ExtraUI extraUiRef;', 'private ExtraUI extraUiRef;\n        private SettingsUI settingsUiRef;')

# Save the reference in CreateSettingsUI
text = text.replace('SettingsUI settingsUi = settingsRoot.AddComponent<SettingsUI>();', 'SettingsUI settingsUi = settingsRoot.AddComponent<SettingsUI>();\n            settingsUiRef = settingsUi;')

# Use it in CreateGlobalUI
text = text.replace('var settingsUI = Object.FindFirstObjectByType<SettingsUI>(UnityEngine.FindObjectsInactive.Include);', 'var settingsUI = settingsUiRef;')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed SettingsUI reference in CreateGlobalUI')
