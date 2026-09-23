import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LanguageUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target1 = '''        [SerializeField] private GameObject panelRoot;
        [SerializeField] private Button[] languageButtons;
        [SerializeField] private Button closeButton;'''

replacement1 = '''        [SerializeField] private GameObject panelRoot;
        [SerializeField] private Button[] languageButtons;
        [SerializeField] private Button closeButton;
        [SerializeField] private TextMeshProUGUI titleText;
        [SerializeField] private Text closeText;'''

target2 = '''        private void UpdateLanguageButtonsUI()
        {
            if (languageButtons == null) return;'''

replacement2 = '''        private void UpdateLanguageButtonsUI()
        {
            if (titleText != null)
            {
                if (SettingsData.Language == GameLanguage.English) titleText.text = "Language Settings";
                else if (SettingsData.Language == GameLanguage.Japanese) titleText.text = "言語設定";
                else if (SettingsData.Language == GameLanguage.ChineseSimplified) titleText.text = "语言设置";
                else if (SettingsData.Language == GameLanguage.ChineseTraditional) titleText.text = "語言設定";
                else titleText.text = "언어 설정";
            }
            if (closeText != null)
            {
                if (SettingsData.Language == GameLanguage.English) closeText.text = "Close";
                else if (SettingsData.Language == GameLanguage.Japanese) closeText.text = "閉じる";
                else if (SettingsData.Language == GameLanguage.ChineseSimplified) closeText.text = "关闭";
                else if (SettingsData.Language == GameLanguage.ChineseTraditional) closeText.text = "關閉";
                else closeText.text = "닫기";
            }

            if (languageButtons == null) return;'''

text = text.replace(target1, replacement1).replace(target2, replacement2)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)
print('Updated LanguageUI.cs to translate title and close button')
