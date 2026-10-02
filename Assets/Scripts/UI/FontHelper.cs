using System.Collections.Generic;
using UnityEngine;
using HalloweenVN.Core;
using UnityEngine.UI;
using TMPro;

namespace HalloweenVN.UI {
    public static class FontHelper {
        private static Dictionary<string, Font> _legacyFontCache = new Dictionary<string, Font>();
        private static Dictionary<string, TMP_FontAsset> _tmpFontCache = new Dictionary<string, TMP_FontAsset>();
        
        public static Font GetFont(string name) {
            if (string.IsNullOrEmpty(name)) return null;
            if (_legacyFontCache.ContainsKey(name)) return _legacyFontCache[name];
            Font rawFont = Resources.Load<Font>("Fonts/" + name);
            if (rawFont != null) _legacyFontCache[name] = rawFont;
            return rawFont;
        }

        private static TMP_FontAsset GetKoreanFallback() {
            if (_tmpFontCache.ContainsKey("KoreanFallback")) return _tmpFontCache["KoreanFallback"];

            TMP_FontAsset prebakedSdf = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
            if (prebakedSdf != null) {
                // To fix missing characters (□), create a lightweight dynamic fallback using the original TTF
                if (prebakedSdf.fallbackFontAssetTable == null)
                    prebakedSdf.fallbackFontAssetTable = new System.Collections.Generic.List<TMP_FontAsset>();
                    
                Font fallbackRawFont = GetFont("MalgunGothic");
                if (fallbackRawFont != null) {
                    bool hasDynamic = false;
                    foreach (var fb in prebakedSdf.fallbackFontAssetTable) {
                        if (fb != null && fb.name == "KoreanFallback Dynamic Addition") hasDynamic = true;
                    }
                    
                    if (!hasDynamic) {
                        TMP_FontAsset dynamicFallback = TMP_FontAsset.CreateFontAsset(fallbackRawFont);
                        dynamicFallback.name = "KoreanFallback Dynamic Addition";
                        prebakedSdf.fallbackFontAssetTable.Add(dynamicFallback);
                    }
                }
                
                _tmpFontCache["KoreanFallback"] = prebakedSdf;
                return prebakedSdf;
            }

            Font rawFont = GetFont("MalgunGothic");
            if (rawFont != null) {
                TMP_FontAsset dynamicFallback = TMP_FontAsset.CreateFontAsset(rawFont);
                dynamicFallback.name = "KoreanFallback SDF";
                _tmpFontCache["KoreanFallback"] = dynamicFallback;
                return dynamicFallback;
            }
            return null;
        }

        public static TMP_FontAsset GetTMPFont(string name) {
            if (string.IsNullOrEmpty(name)) return null;
            if (_tmpFontCache.ContainsKey(name)) return _tmpFontCache[name];

            // 1. Try to load pre-made SDF asset
            TMP_FontAsset sdf = Resources.Load<TMP_FontAsset>("Fonts/" + name + " SDF");
            if (sdf != null) {
                // Ensure fallback exists even for pre-made SDFs
                if (sdf.fallbackFontAssetTable == null)
                    sdf.fallbackFontAssetTable = new System.Collections.Generic.List<TMP_FontAsset>();
                
                bool hasFallback = false;
                foreach (var fb in sdf.fallbackFontAssetTable) {
                    if (fb != null && fb.name.Contains("KoreanFallback")) {
                        hasFallback = true;
                        break;
                    }
                }
                
                if (!hasFallback) {
                    TMP_FontAsset fallback = GetKoreanFallback();
                    if (fallback != null && sdf != fallback) sdf.fallbackFontAssetTable.Add(fallback);
                }
                
                // Adjust scales for notoriously large fonts
                if (name == "MaShanZheng-Regular") {
                    var info = sdf.faceInfo;
                    info.scale = 0.8f; 
                    sdf.faceInfo = info;
                }

                _tmpFontCache[name] = sdf;
                return sdf;
            }

            // 2. If no pre-made SDF, load raw TTF and convert at runtime
            Font rawFont = GetFont(name);
            if (rawFont != null) {
                TMP_FontAsset dynamicSdf = TMP_FontAsset.CreateFontAsset(rawFont);
                dynamicSdf.name = name + " Runtime SDF";
                
                // Add fallback for missing characters (like Japanese quotes 「 」)
                if (dynamicSdf.fallbackFontAssetTable == null)
                    dynamicSdf.fallbackFontAssetTable = new System.Collections.Generic.List<TMP_FontAsset>();
                
                TMP_FontAsset fallback = GetKoreanFallback();
                if (fallback != null) dynamicSdf.fallbackFontAssetTable.Add(fallback);
                
                _tmpFontCache[name] = dynamicSdf;
                return dynamicSdf;
            }

            return null;
        }

        public static string GetFontNameForLanguage(GameLanguage lang) {
            if (!SettingsData.UseHandwritingFont) return "MalgunGothic";
            switch (lang) {
                case GameLanguage.English: return "Caveat-Regular";
                case GameLanguage.Japanese: return "YujiSyuku-Regular";
                case GameLanguage.ChineseSimplified: return "MaShanZheng-Regular";
                case GameLanguage.ChineseTraditional: return "YujiSyuku-Regular";
                default: return "NanumPenScript";
            }
        }
    }
}