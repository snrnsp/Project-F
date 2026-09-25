import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

text = text.replace('CreateSettingsLabel(panel.transform, "텍스트 속도", yPos)', 'CreateSettingsLabel(panel.transform, "텍스트 속도", yPos + 15f)')
text = text.replace('CreateSettingsLabel(panel.transform, "BGM", yPos)', 'CreateSettingsLabel(panel.transform, "BGM", yPos + 15f)')
text = text.replace('CreateSettingsLabel(panel.transform, "SFX", yPos)', 'CreateSettingsLabel(panel.transform, "SFX", yPos + 15f)')

with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
    f.write(text)
print('Labels moved up by 15f')
