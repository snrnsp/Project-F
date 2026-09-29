import sys

path = 'F:/Project-F/Assets/Scripts/UI/LanguageUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()
    
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'private void SetLanguage(GameLanguage lang)' in line:
        start_idx = i
    if start_idx != -1 and 'Debug.Log($"Language set to {lang}");' in line:
        end_idx = i + 2
        break
        
if start_idx != -1 and end_idx != -1:
    new_method = """        private void SetLanguage(GameLanguage lang)
        {
            SettingsData.Language = lang;
            SettingsData.Save();
            UpdateLanguageButtonsUI();

            LobbyUI lobby = Object.FindAnyObjectByType<LobbyUI>();
            if (lobby != null) lobby.UpdateLanguage();

            SettingsUI settings = Object.FindAnyObjectByType<SettingsUI>(FindObjectsInactive.Include);
            if (settings != null) settings.UpdateLanguage();

            DialogueUI dialogue = Object.FindAnyObjectByType<DialogueUI>(FindObjectsInactive.Include);
            if (dialogue != null) dialogue.UpdateLanguage();

            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(lang);
            var tmpFont = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            if (tmpFont != null)
            {
                var allTmp = Resources.FindObjectsOfTypeAll<TMPro.TextMeshProUGUI>();
                foreach (var tmp in allTmp)
                {
                    if (tmp.gameObject.scene.name != null)
                    {
                        tmp.font = tmpFont;
                    }
                }
            }

            Debug.Log($"Language set to {lang}");
        }\n"""
    
    lines = lines[:start_idx] + [new_method] + lines[end_idx:]
    with open(path, 'w', encoding='utf-8-sig') as fw:
        fw.writelines(lines)
    print("Success")
