import sys
import re

path = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace declaration
content = content.replace('[SerializeField] private Text lobbyTitleText;', '[SerializeField] private Image logoImage;')

# Remove font setting for lobbyTitleText
content = re.sub(r'if \(lobbyTitleText != null\) lobbyTitleText\.font = f;\n?', '', content)

# Remove text translations for lobbyTitleText
content = re.sub(r'if \(lobbyTitleText != null\) lobbyTitleText\.text = "[^"]+";\n?', '', content)

# Inject logo loading at the beginning of UpdateLanguage
old_update_lang = """    public void UpdateLanguage()
    {
        if (newGameText == null) return;

        GameLanguage lang = SettingsData.Language;"""

new_update_lang = """    public void UpdateLanguage()
    {
        if (logoImage != null)
        {
            Sprite logoSprite = Resources.Load<Sprite>("Images/Logos/logo_en");
            if (logoSprite != null) logoImage.sprite = logoSprite;
        }

        if (newGameText == null) return;

        GameLanguage lang = SettingsData.Language;"""

content = content.replace(old_update_lang, new_update_lang)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("LobbyUI updated for Logo")
