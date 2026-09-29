import sys

path = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

start_idx = -1
for i, line in enumerate(lines):
    if 'public void UpdateLanguage()' in line:
        start_idx = i
        break

if start_idx != -1:
    new_code = """    public void UpdateLanguage()
    {
        GameLanguage lang = SettingsData.Language;
        
        if (logoImage != null)
        {
            string logoPath = "Images/Logos/logo_en";
            if (lang == GameLanguage.Korean)
            {
                logoPath = "Images/Logos/logo_ko";
            }
            Sprite logoSprite = Resources.Load<Sprite>(logoPath);
            if (logoSprite != null) 
            {
                logoImage.sprite = logoSprite;
                logoImage.color = Color.white; // ensure it's not tinted
            }
        }

        if (newGameText == null) return;
"""
    # Remove old start
    del lines[start_idx:start_idx+4]
    # Insert new code
    lines.insert(start_idx, new_code)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(lines)
print("LobbyUI UpdateLanguage fixed")
