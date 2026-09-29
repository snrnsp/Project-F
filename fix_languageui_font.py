import sys
sys.stdout.reconfigure(encoding='utf-8')

path = 'F:/Project-F/Assets/Scripts/UI/LanguageUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_str = """        private void SetLanguage(GameLanguage lang)
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

            Debug.Log($"Language set to {lang}");
        }"""

new_str = """        private void SetLanguage(GameLanguage lang)
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

            // Globally update all TextMeshProUGUI instances to the new font
            string fontName = FontHelper.GetFontNameForLanguage(lang);
            var tmpFont = FontHelper.GetTMPFont(fontName);
            if (tmpFont != null)
            {
                var allTmp = Resources.FindObjectsOfTypeAll<TMPro.TextMeshProUGUI>();
                foreach (var tmp in allTmp)
                {
                    if (tmp.gameObject.scene.name != null) // Only objects in the active scene
                    {
                        tmp.font = tmpFont;
                    }
                }
            }

            Debug.Log($"Language set to {lang}");
        }"""

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("✅ LanguageUI.cs 폰트 동기화 로직 적용 완료")
else:
    print("❌ SetLanguage 부분을 찾지 못했습니다.")
