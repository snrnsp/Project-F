import sys
import re

path = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Lines 185-186
content = re.sub(
    r'if \(autoPlayValueText != null\)\s*autoPlayValueText\.text = SettingsData\.AutoPlayDelay\.ToString\("0\.0"\);',
    r'if (autoPlayInputField != null) { autoPlayInputField.text = SettingsData.AutoPlayDelay.ToString("0.0"); if (autoPlayInputField.textComponent != null) autoPlayInputField.textComponent.font = f; }',
    content,
    count=1
)

# Any other remaining instances (like line 303)
content = re.sub(
    r'if \(autoPlayValueText != null\)\s*autoPlayValueText\.text = SettingsData\.AutoPlayDelay\.ToString\("0\.0"\);',
    r'if (autoPlayInputField != null) autoPlayInputField.text = SettingsData.AutoPlayDelay.ToString("0.0");',
    content
)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print('SettingsUI fixed')
