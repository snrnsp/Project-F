import sys

path = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Add listener to OnEnable
content = content.replace('UpdateAllLabels();', 'if (autoPlayInputField != null) autoPlayInputField.onEndEdit.AddListener(OnAutoPlayInputEdit);\n        UpdateAllLabels();', 1)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("SettingsUI listener finally added")
