using UnityEngine;
using UnityEditor;

public class FontCheckEditor {
    [MenuItem("Tools/Check Font")]
    public static void Check() {
        string[] fontNames = { "LongCang-Regular", "MaShanZheng-Regular", "ZenKurenaido-Regular", "YujiSyuku-Regular", "NanumPenScript" };
        string testChars = "語言設定文本速度背景音樂音效關閉简体中文繁體한국어";
        
        foreach(var fontName in fontNames) {
            Font f = Resources.Load<Font>("Fonts/" + fontName);
            if (f != null) {
                f.RequestCharactersInTexture(testChars);
                string missing = "";
                foreach(char c in testChars) {
                    if (!f.HasCharacter(c)) missing += c;
                }
                Debug.Log(fontName + " missing: " + (missing.Length == 0 ? "NONE" : missing));
            }
        }
    }
}