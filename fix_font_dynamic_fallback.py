import sys

path = 'F:/Project-F/Assets/Scripts/UI/FontHelper.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Add GetKoreanFallback method inside FontHelper
fallback_method = """        private static TMP_FontAsset GetKoreanFallback() {
            if (_tmpFontCache.ContainsKey("KoreanFallback")) return _tmpFontCache["KoreanFallback"];
            Font rawFont = GetFont("MalgunGothic");
            if (rawFont != null) {
                TMP_FontAsset dynamicFallback = TMP_FontAsset.CreateFontAsset(rawFont);
                dynamicFallback.name = "KoreanFallback SDF";
                _tmpFontCache["KoreanFallback"] = dynamicFallback;
                return dynamicFallback;
            }
            return null;
        }

        public static TMP_FontAsset GetTMPFont(string name) {"""

if 'private static TMP_FontAsset GetKoreanFallback()' not in content:
    content = content.replace('public static TMP_FontAsset GetTMPFont(string name) {', fallback_method)

# Replace the fallback loading logic
old_load = 'TMP_FontAsset fallback = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");'
new_load = 'TMP_FontAsset fallback = GetKoreanFallback();'

content = content.replace(old_load, new_load)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("FontHelper.cs fallback updated to dynamic")
