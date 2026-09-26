import io
import sys

file_path = 'Assets/Scripts/UI/LobbyUI.cs'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('            if (lang == GameLanguage.Korean)')
end_idx = content.find('        private void Start()')
if start_idx != -1 and end_idx != -1:
    replacement_block = '''            if (lang == GameLanguage.Korean)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "오블리비언";
                if (lobbySubtitleText != null) lobbySubtitleText.text = "OBLIVION";
                if (newGameText != null) newGameText.text = "새 게임";
                if (extraText != null) extraText.text = "캐릭터";
                if (settingsText != null) settingsText.text = "환경 설정";
                if (languageBtnText != null) languageBtnText.text = "Language";
                if (versionText != null) versionText.text = "버전 1.0.2";
            }
            // English
            else if (lang == GameLanguage.English)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "OBLIVION";
                if (lobbySubtitleText != null) lobbySubtitleText.text = "";
                if (newGameText != null) newGameText.text = "New Game";
                if (extraText != null) extraText.text = "Characters";
                if (settingsText != null) settingsText.text = "Settings";
                if (languageBtnText != null) languageBtnText.text = "Language";
                if (versionText != null) versionText.text = "Ver 1.0.2";
            }
            // Japanese
            else if (lang == GameLanguage.Japanese)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "忘却";
                if (lobbySubtitleText != null) lobbySubtitleText.text = "OBLIVION";
                if (newGameText != null) newGameText.text = "はじめから";
                if (extraText != null) extraText.text = "キャラクター";
                if (settingsText != null) settingsText.text = "設定";
                if (languageBtnText != null) languageBtnText.text = "Language";
                if (versionText != null) versionText.text = "バージョン 1.0.2";
            }
            // Simplified Chinese
            else if (lang == GameLanguage.ChineseSimplified)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "遗忘";
                if (lobbySubtitleText != null) lobbySubtitleText.text = "OBLIVION";
                if (newGameText != null) newGameText.text = "新游戏";
                if (extraText != null) extraText.text = "角色";
                if (settingsText != null) settingsText.text = "设置";
                if (languageBtnText != null) languageBtnText.text = "Language";
                if (versionText != null) versionText.text = "版本 1.0.2";
            }
            // Traditional Chinese
            else if (lang == GameLanguage.ChineseTraditional)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "遺忘";
                if (lobbySubtitleText != null) lobbySubtitleText.text = "OBLIVION";
                if (newGameText != null) newGameText.text = "新遊戲";
                if (extraText != null) extraText.text = "角色";
                if (settingsText != null) settingsText.text = "設定";
                if (languageBtnText != null) languageBtnText.text = "Language";
                if (versionText != null) versionText.text = "版本 1.0.2";
            }
'''
    new_content = content[:start_idx] + replacement_block + content[end_idx:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('SUCCESS')
else:
    print('FAILED TO FIND BOUNDARIES')
