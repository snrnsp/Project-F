import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

# 1. Update Show() to call RefreshLanguage()
target_show = """        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
            if (extraPanel != null)
            {
                extraPanel.SetActive(true);
                SelectCharacter(0);
            }"""

replacement_show = """        public void Show()
        {
            if (EventSystem.current != null) EventSystem.current.SetSelectedGameObject(null);
            
            // Re-initialize language dynamically every time we open the book!
            InitializeProfiles();
            UpdateTabNames();

            if (extraPanel != null)
            {
                extraPanel.SetActive(true);
                SelectCharacter(currentIndex); // Refresh current selection
            }"""

if target_show in text:
    text = text.replace(target_show, replacement_show)

# 2. Add UpdateTabNames() method and modify the labels in profileTxt
target_labels = """            if (profileTxt != null)
            {
                profileTxt.text =
                    $"<color=#B46420>나이:</color> {profile.age}\\n" +
                    $"<color=#B46420>역할:</color> {profile.role}\\n" +
                    $"<color=#B46420>MBTI:</color> {profile.mbti}\\n\\n" +
                    $"<color=#B46420>외모:</color> {profile.appearance}\\n\\n" +
                    $"<color=#B46420>성격:</color> {profile.personality}\\n\\n" +
                    $"<color=#B46420>말투:</color> {profile.speechStyle}\\n\\n" +
                    $"<color=#B46420>비밀:</color> {profile.secret}";
            }"""

replacement_labels = """        private void UpdateTabNames()
        {
            for (int i = 0; i < folderTabTexts.Count; i++)
            {
                if (i < profiles.Count && folderTabTexts[i] != null)
                {
                    folderTabTexts[i].text = profiles[i].name;
                }
            }
        }

        private string GetLabel(string ko, string en, string jp, string zh)
        {
            switch (HalloweenVN.Core.SettingsData.Language)
            {
                case HalloweenVN.Core.GameLanguage.English: return en;
                case HalloweenVN.Core.GameLanguage.Japanese: return jp;
                case HalloweenVN.Core.GameLanguage.ChineseSimplified: 
                case HalloweenVN.Core.GameLanguage.ChineseTraditional: return zh;
                default: return ko;
            }
        }

        private void UpdateProfileText(TextMeshProUGUI profileTxt, CharacterProfile profile)
        {
            if (profileTxt == null) return;
            string l_age = GetLabel("나이", "Age", "年齢", "年龄");
            string l_role = GetLabel("역할", "Role", "役割", "职责");
            string l_mbti = "MBTI";
            string l_app = GetLabel("외모", "Appearance", "外見", "外貌");
            string l_pers = GetLabel("성격", "Personality", "性格", "性格");
            string l_speech = GetLabel("말투", "Speech", "口調", "语气");
            string l_secret = GetLabel("비밀", "Secret", "秘密", "秘密");

            profileTxt.text =
                $"<color=#B46420>{l_age}:</color> {profile.age}\n" +
                $"<color=#B46420>{l_role}:</color> {profile.role}\n" +
                $"<color=#B46420>{l_mbti}:</color> {profile.mbti}\n\n" +
                $"<color=#B46420>{l_app}:</color> {profile.appearance}\n\n" +
                $"<color=#B46420>{l_pers}:</color> {profile.personality}\n\n" +
                $"<color=#B46420>{l_speech}:</color> {profile.speechStyle}\n\n" +
                $"<color=#B46420>{l_secret}:</color> {profile.secret}";
        }"""

if target_labels in text:
    text = text.replace(target_labels, "")
    text = text.replace("if (nameTxt != null) nameTxt.text = profile.name;", "if (nameTxt != null) nameTxt.text = profile.name;\n            UpdateProfileText(profileTxt, profile);")
    text = text.replace("public void SelectCharacter(int index)", replacement_labels + "\n\n        public void SelectCharacter(int index)")

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)
print("Updated ExtraUI for dynamic language refresh and localized labels!")
