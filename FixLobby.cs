using System.IO;
using System.Text;
using System;

class Program {
    static void Main() {
        string path = "Assets/Scripts/UI/LobbyUI.cs";
        string content = File.ReadAllText(path, Encoding.UTF8);
        string startStr = "if (lang == GameLanguage.Korean)";
        string endStr = "private void Start()";
        
        int startIdx = content.IndexOf(startStr);
        int endIdx = content.IndexOf(endStr);
        
        string newBlock = 
@"if (lang == GameLanguage.Korean)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "오블리비언\n<size=22>OBLIVION</size>";
                if (newGameText != null) newGameText.text = "새 게임";
                if (extraText != null) extraText.text = "캐릭터";
                if (settingsText != null) settingsText.text = "환경 설정";
                if (languageBtnText != null) languageBtnText.text = "언어 설정";
                if (versionText != null) versionText.text = "버전 1.0.2";
            }
            // English
            else if (lang == GameLanguage.English)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "OBLIVION";
                if (newGameText != null) newGameText.text = "New Game";
                if (extraText != null) extraText.text = "Characters";
                if (settingsText != null) settingsText.text = "Settings";
                if (languageBtnText != null) languageBtnText.text = "Language";
                if (versionText != null) versionText.text = "Ver 1.0.2";
            }
            // Japanese
            else if (lang == GameLanguage.Japanese)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "忘却\n<size=22>OBLIVION</size>";
                if (newGameText != null) newGameText.text = "はじめから";
                if (extraText != null) extraText.text = "キャラクター";
                if (settingsText != null) settingsText.text = "設定";
                if (languageBtnText != null) languageBtnText.text = "言語設定";
                if (versionText != null) versionText.text = "バージョン 1.0.2";
            }
            // Simplified Chinese
            else if (lang == GameLanguage.ChineseSimplified)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "遗忘\n<size=22>OBLIVION</size>";
                if (newGameText != null) newGameText.text = "新游戏";
                if (extraText != null) extraText.text = "角色";
                if (settingsText != null) settingsText.text = "设置";
                if (languageBtnText != null) languageBtnText.text = "语言设置";
                if (versionText != null) versionText.text = "版本 1.0.2";
            }
            // Traditional Chinese
            else if (lang == GameLanguage.ChineseTraditional)
            {
                if (lobbyTitleText != null) lobbyTitleText.text = "遺忘\n<size=22>OBLIVION</size>";
                if (newGameText != null) newGameText.text = "新遊戲";
                if (extraText != null) extraText.text = "角色";
                if (settingsText != null) settingsText.text = "設定";
                if (languageBtnText != null) languageBtnText.text = "語言設定";
                if (versionText != null) versionText.text = "版本 1.0.2";
            }
        }

        ";
        
        string newContent = content.Substring(0, startIdx) + newBlock + content.Substring(endIdx);
        File.WriteAllText(path, newContent, new UTF8Encoding(true));
        Console.WriteLine("Done");
    }
}