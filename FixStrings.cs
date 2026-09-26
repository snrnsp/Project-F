using System;
using System.IO;
using System.Text;

class Program {
    static void Main() {
        string path = @"Assets\Scripts\UI\LobbyUI.cs";
        string content = File.ReadAllText(path, new UTF8Encoding(false));
        
        int startIdx = content.IndexOf("            if (lang == GameLanguage.Korean)");
        int endIdx = content.IndexOf("        private void Start()");
        
        if (startIdx != -1 && endIdx != -1) {
            string replacement = @"            if (lang == GameLanguage.Korean)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = ""오블리비언"";
                if (lobbySubtitleText != null) lobbySubtitleText.text = ""OBLIVION"";
                if (newGameText != null) newGameText.text = ""새 게임"";
                if (extraText != null) extraText.text = ""캐릭터"";
                if (settingsText != null) settingsText.text = ""환경 설정"";
                if (languageBtnText != null) languageBtnText.text = ""Language"";
                if (versionText != null) versionText.text = ""버전 1.0.2"";
            }
            // English
            else if (lang == GameLanguage.English)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = ""OBLIVION"";
                if (lobbySubtitleText != null) lobbySubtitleText.text = """";
                if (newGameText != null) newGameText.text = ""New Game"";
                if (extraText != null) extraText.text = ""Characters"";
                if (settingsText != null) settingsText.text = ""Settings"";
                if (languageBtnText != null) languageBtnText.text = ""Language"";
                if (versionText != null) versionText.text = ""Ver 1.0.2"";
            }
            // Japanese
            else if (lang == GameLanguage.Japanese)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = ""忘却"";
                if (lobbySubtitleText != null) lobbySubtitleText.text = ""OBLIVION"";
                if (newGameText != null) newGameText.text = ""はじめから"";
                if (extraText != null) extraText.text = ""キャラクター"";
                if (settingsText != null) settingsText.text = ""設定"";
                if (languageBtnText != null) languageBtnText.text = ""Language"";
                if (versionText != null) versionText.text = ""バージョン 1.0.2"";
            }
            // Simplified Chinese
            else if (lang == GameLanguage.ChineseSimplified)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = ""遗忘"";
                if (lobbySubtitleText != null) lobbySubtitleText.text = ""OBLIVION"";
                if (newGameText != null) newGameText.text = ""新游戏"";
                if (extraText != null) extraText.text = ""角色"";
                if (settingsText != null) settingsText.text = ""设置"";
                if (languageBtnText != null) languageBtnText.text = ""Language"";
                if (versionText != null) versionText.text = ""版本 1.0.2"";
            }
            // Traditional Chinese
            else if (lang == GameLanguage.ChineseTraditional)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = ""遺忘"";
                if (lobbySubtitleText != null) lobbySubtitleText.text = ""OBLIVION"";
                if (newGameText != null) newGameText.text = ""新遊戲"";
                if (extraText != null) extraText.text = ""角色"";
                if (settingsText != null) settingsText.text = ""設定"";
                if (languageBtnText != null) languageBtnText.text = ""Language"";
                if (versionText != null) versionText.text = ""版本 1.0.2"";
            }
";
            content = content.Substring(0, startIdx) + replacement + "        private void Start()" + content.Substring(endIdx + 28);
            File.WriteAllText(path, content, new UTF8Encoding(true));
            Console.WriteLine("SUCCESS");
        } else {
            Console.WriteLine("FAILED");
        }
    }
}
