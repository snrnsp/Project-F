import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Loc.Get("ui.settings.text_speed", "텍스트 속도")', 'Loc.Get("ui.settings.text_speed", "텍스트 속도 조절")')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated SettingsUI.cs text speed label.")
