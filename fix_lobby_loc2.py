import codecs

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

bad_str = """            var loadTuple = CreateLegacyButton(lobbyPanelRoot.transform, "\uc774\uc5b4\ud558\uae30", 260, 55, btnBg);
            UIHelper.SetAnchors(loadTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            loadTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var startTuple = CreateLegacyButton(lobbyPanelRoot.transform, "\uc0c8 \uac8c\uc784", 260, 55, btnBg);
            UIHelper.SetAnchors(startTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            startTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var extraTuple = CreateLegacyButton(lobbyPanelRoot.transform, "\uce90\ub9ad\ud130", 260, 55, btnBg);
            UIHelper.SetAnchors(extraTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            extraTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var langTuple = CreateLegacyButton(lobbyPanelRoot.transform, "Language", 260, 55, btnBg);
            UIHelper.SetAnchors(langTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            langTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var settingsTuple = CreateLegacyButton(lobbyPanelRoot.transform, "\ud658\uacbd \uc124\uc815", 260, 55, btnBg);
            lobbySettingsBtnObj = settingsTuple.btn.gameObject;
            UIHelper.SetAnchors(settingsTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            settingsTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));"""

good_str = """            string t_continue = "\uc774\uc5b4\ud558\uae30";
            string t_newgame = "\uc0c8 \uac8c\uc784";
            string t_extra = "\uce90\ub9ad\ud130";
            string t_lang = "Language";
            string t_settings = "\ud658\uacbd \uc124\uc815";

            switch (SettingsData.Language)
            {
                case GameLanguage.English:
                    t_continue = "Continue"; t_newgame = "New Game"; t_extra = "Characters"; t_settings = "Settings";
                    break;
                case GameLanguage.Japanese:
                    t_continue = "\u7d9a\u304d\u304b\u3089"; t_newgame = "\u521d\u3081\u304b\u3089"; t_extra = "\u30ad\u30e3\u30e9\u30af\u30bf\u30fc"; t_settings = "\u8a2d\u5b9a";
                    break;
                case GameLanguage.ChineseSimplified:
                    t_continue = "\u7ee7\u7eed\u6e38\u620f"; t_newgame = "\u65b0\u6e38\u620f"; t_extra = "\u89d2\u8272\u6863\u6848"; t_settings = "\u8bbe\u7f6e";
                    break;
                case GameLanguage.ChineseTraditional:
                    t_continue = "\u7e7c\u7e8c\u904a\u6232"; t_newgame = "\u65b0\u904a\u6232"; t_extra = "\u89d2\u8272\u6a94\u6848"; t_settings = "\u8a2d\u7f6e";
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
            lobbySettingsBtnObj = settingsTuple.btn.gameObject;
            UIHelper.SetAnchors(settingsTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            settingsTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));"""

# handle windows newlines
bad_str_win = bad_str.replace('\n', '\r\n')

if bad_str_win in text:
    text = text.replace(bad_str_win, good_str)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Fixed lobby buttons localization (win lf)!")
else:
    if bad_str in text:
        text = text.replace(bad_str, good_str)
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(text)
        print("Fixed lobby buttons localization (lf)!")
    else:
        print("COULD NOT FIND BLOCK")
