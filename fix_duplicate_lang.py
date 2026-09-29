import sys

path = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'GameLanguage lang = SettingsData.Language;' in line and i > 50:
        del lines[i]
        break

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("Removed duplicate variable declaration")
