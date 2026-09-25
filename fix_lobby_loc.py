import codecs, re

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

# Replace hardcoded button strings with a language switch
replacement = """
            string t_continue = "이어하기";
            string t_newgame = "새 게임";
            string t_extra = "캐릭터";
            string t_lang = "Language";
            string t_settings = "환경 설정";
            string t_exit = "종료";

            switch (SettingsData.Language)
            {
                case GameLanguage.English:
                    t_continue = "Continue"; t_newgame = "New Game"; t_extra = "Characters"; t_settings = "Settings"; t_exit = "Exit";
                    break;
                case GameLanguage.Japanese:
                    t_continue = "続きから"; t_newgame = "初めから"; t_extra = "キャラクター"; t_settings = "設定"; t_exit = "終了";
                    break;
                case GameLanguage.ChineseSimplified:
                    t_continue = "继续游戏"; t_newgame = "新游戏"; t_extra = "角色档案"; t_settings = "设置"; t_exit = "退出";
                    break;
                case GameLanguage.ChineseTraditional:
                    t_continue = "繼續遊戲"; t_newgame = "新遊戲"; t_extra = "角色檔案"; t_settings = "設置"; t_exit = "退出";
                    break;
            }

            var loadTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_continue, 260, 55, btnBg);
            UIHelper.SetAnchors(loadTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            loadTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var startTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_newgame, 260, 55, btnBg);
            UIHelper.SetAnchors(startTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            startTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var extraTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_extra, 260, 55, btnBg);
            UIHelper.SetAnchors(extraTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            extraTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var langTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_lang, 260, 55, btnBg);
            UIHelper.SetAnchors(langTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            langTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var settingsTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_settings, 260, 55, btnBg);
            UIHelper.SetAnchors(settingsTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            settingsTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));

            var exitTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_exit, 260, 55, btnBg);
"""

# Find the block to replace
start_idx = text.find('var loadTuple = CreateLegacyButton(lobbyPanelRoot.transform, "이어하기", 260, 55, btnBg);')
end_idx = text.find('UIHelper.SetAnchors(exitTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));')
end_idx = text.find('\n', end_idx) + 1

if start_idx != -1 and end_idx != -1:
    text = text[:start_idx] + replacement.strip() + '\n' + text[end_idx:]
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Replaced lobby buttons with localized variables!")
else:
    print("Could not find lobby buttons block to replace.")
