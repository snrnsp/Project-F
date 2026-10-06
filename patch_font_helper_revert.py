import re

with open('Assets/Scripts/UI/FontHelper.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

new_fallback = '''        private static TMP_FontAsset GetKoreanFallback() {
            if (_tmpFontCache.ContainsKey("KoreanFallback")) return _tmpFontCache["KoreanFallback"];
            TMP_FontAsset prebakedSdf = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
            if (prebakedSdf != null) {
                // Fix missing characters by creating a lightweight dynamic fallback using the original TTF
                if (prebakedSdf.fallbackFontAssetTable == null)
                    prebakedSdf.fallbackFontAssetTable = new System.Collections.Generic.List<TMP_FontAsset>();
                    
                Font fallbackRawFont = GetFont("MalgunGothic");
                if (fallbackRawFont != null) {
                    bool hasDynamic = false;
                    foreach (var fb in prebakedSdf.fallbackFontAssetTable) {
                        if (fb != null && fb.name == "KoreanFallback Dynamic Addition") { hasDynamic = true; break; }
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
            
            // If SDF is missing entirely
            Font rawFont = GetFont("MalgunGothic");
            if (rawFont != null) {
                TMP_FontAsset dynamicFallback = TMP_FontAsset.CreateFontAsset(rawFont);
                dynamicFallback.name = "KoreanFallback SDF";
                _tmpFontCache["KoreanFallback"] = dynamicFallback;
                return dynamicFallback;
            }
            return null;
        }'''

content = re.sub(r'        private static TMP_FontAsset GetKoreanFallback\(\) \{.*?\n        \}', new_fallback, content, flags=re.DOTALL)

with open('Assets/Scripts/UI/FontHelper.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("Restored fallback in FontHelper.cs")
