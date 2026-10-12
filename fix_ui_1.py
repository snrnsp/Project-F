import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'float startY = 120f; // Center adjusted for 4 buttons' in line:
        start_idx = i
    if 'Button settingsBtn = settingsTuple.btn;' in line and start_idx != -1:
        end_idx = i
        break

print(f"Start: {start_idx}, End: {end_idx}")

new_code = '''            float startY = 160f; // Center adjusted for 5 buttons
            float spacing = 80f;
            int i = 0;

            // Same keys as LobbyUI.UpdateLanguage (which refreshes these on language change).
            string t_newgame = Loc.Get("ui.lobby.new_game", "새게임");
            string t_continue = Loc.Get("ui.lobby.continue", "이어하기");
            string t_extra = Loc.Get("ui.lobby.characters", "캐릭터");
            string t_lang = Loc.Get("ui.lobby.language", "Language");
            string t_settings = Loc.Get("ui.lobby.settings", "환경 설정");

            var startTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_newgame, 260, 55, btnBg);
            UIHelper.SetAnchors(startTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            startTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(245, startY - (spacing * i++));
            
            var continueTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_continue, 260, 55, btnBg);
            UIHelper.SetAnchors(continueTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            continueTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(245, startY - (spacing * i++));

            var extraTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_extra, 260, 55, btnBg);
            UIHelper.SetAnchors(extraTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            extraTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(245, startY - (spacing * i++));
            
            var langTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_lang, 260, 55, btnBg);
            UIHelper.SetAnchors(langTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            langTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(245, startY - (spacing * i++));
            
            var settingsTuple = CreateLegacyButton(lobbyPanelRoot.transform, t_settings, 260, 55, btnBg);
            lobbySettingsBtnObj = settingsTuple.btn.gameObject;
            UIHelper.SetAnchors(settingsTuple.btn.GetComponent<RectTransform>(), new Vector2(0, 0.5f), new Vector2(0, 0.5f), new Vector2(0, 0.5f));
            settingsTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(245, startY - (spacing * i++));
            
            langButtonRef = langTuple.btn;
            
            // Bottom text removed per user request

            // Version Text (Bottom Left)
            // GameObject verObj = UIHelper.CreateUIObject("VersionText", lobbyPanelRoot.transform);
            // RectTransform verRt = verObj.GetComponent<RectTransform>();
            // UIHelper.SetAnchors(verRt, new Vector2(0, 0), new Vector2(0, 0), new Vector2(0, 0));
            // verRt.anchoredPosition = new Vector2(20, 20);
            // Text versionText = CreateLegacyText(verObj, "v1.0.0", new Color32(200, 200, 200, 200), 16, TextAnchor.LowerLeft);

            Button newGameBtn = startTuple.btn;
            Button continueBtn = continueTuple.btn;
'''

if start_idx != -1 and end_idx != -1:
    lines[start_idx:end_idx] = [new_code]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Replaced button generation.")
else:
    print("Could not find the block.")
