using System.Collections.Generic;
using UnityEngine;
using HalloweenVN.Core;
using UnityEngine.UI;

namespace HalloweenVN.UI {
    public static class FontHelper {
        private static Dictionary<string, Font> _legacyFontCache = new Dictionary<string, Font>();
        
        public static Font GetFont(string name) {
            if (string.IsNullOrEmpty(name)) return null;
            if (_legacyFontCache.ContainsKey(name)) return _legacyFontCache[name];
            Font rawFont = Resources.Load<Font>("Fonts/" + name);
            if (rawFont != null) _legacyFontCache[name] = rawFont;
            return rawFont;
        }

        public static string GetFontNameForLanguage(GameLanguage lang) {
            switch (lang) {
                case GameLanguage.English: return "Caveat-Regular";
                case GameLanguage.Japanese: return "ZenKurenaido-Regular";
                case GameLanguage.ChineseSimplified: return "MaShanZheng-Regular";
                case GameLanguage.ChineseTraditional: return "ZenKurenaido-Regular"; // NanumPenScript has huge Hanja (Traditional) coverage!
                default: return "NanumPenScript";
            }
        }
    }
}