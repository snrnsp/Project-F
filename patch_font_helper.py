import re

with open('Assets/Scripts/UI/FontHelper.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace GetKoreanFallback logic
new_fallback = '''        private static TMP_FontAsset GetKoreanFallback() {
            if (_tmpFontCache.ContainsKey("KoreanFallback")) return _tmpFontCache["KoreanFallback"];
            TMP_FontAsset prebakedSdf = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
            if (prebakedSdf != null) {
                _tmpFontCache["KoreanFallback"] = prebakedSdf;
                return prebakedSdf;
            }
            return null;
        }'''

content = re.sub(r'        private static TMP_FontAsset GetKoreanFallback\(\) \{.*?\n        \}', new_fallback, content, flags=re.DOTALL)

with open('Assets/Scripts/UI/FontHelper.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("Patched FontHelper.cs")
