import codecs

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

bad_str = """            var loadTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_continue, 260, 55, btnBg);
            UIHelper.SetAnchors(loadTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            loadTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(180, startY - (spacing * i++));
            
            var startTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_newgame, 260, 55, btnBg);"""

good_str = """            var startTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_newgame, 260, 55, btnBg);"""

bad_ref = """            Button continueBtn = loadTuple.btn;
            Button settingsBtn = settingsTuple.btn;

            // Attach LobbyUI
            LobbyUI lobbyUi = lobbyPanelRoot.AddComponent<LobbyUI>();
            UIHelper.SetField(lobbyUi, "lobbyPanel", lobbyPanelRoot);
            UIHelper.SetField(lobbyUi, "titleText", null); // Title text removed
            UIHelper.SetField(lobbyUi, "newGameButton", newGameBtn);
            UIHelper.SetField(lobbyUi, "continueButton", continueBtn);
            
            // Text references for translation
            UIHelper.SetField(lobbyUi, "newGameText", startTuple.text);
            UIHelper.SetField(lobbyUi, "continueText", loadTuple.text);"""

good_ref = """            Button settingsBtn = settingsTuple.btn;

            // Attach LobbyUI
            LobbyUI lobbyUi = lobbyPanelRoot.AddComponent<LobbyUI>();
            UIHelper.SetField(lobbyUi, "lobbyPanel", lobbyPanelRoot);
            UIHelper.SetField(lobbyUi, "titleText", null); // Title text removed
            UIHelper.SetField(lobbyUi, "newGameButton", newGameBtn);
            UIHelper.SetField(lobbyUi, "continueButton", null);
            
            // Text references for translation
            UIHelper.SetField(lobbyUi, "newGameText", startTuple.text);
            UIHelper.SetField(lobbyUi, "continueText", null);"""

# Handle Windows newlines
bad_str_win = bad_str.replace('\n', '\r\n')
bad_ref_win = bad_ref.replace('\n', '\r\n')

if bad_str_win in text and bad_ref_win in text:
    text = text.replace(bad_str_win, good_str.replace('\n', '\r\n'))
    text = text.replace(bad_ref_win, good_ref.replace('\n', '\r\n'))
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Removed continue button (win lf)!")
else:
    if bad_str in text and bad_ref in text:
        text = text.replace(bad_str, good_str)
        text = text.replace(bad_ref, good_ref)
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(text)
        print("Removed continue button (lf)!")
    else:
        print("Could not find the target blocks.")
