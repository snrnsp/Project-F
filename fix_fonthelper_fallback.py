import sys

path = 'F:/Project-F/Assets/Scripts/UI/FontHelper.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_logic = """            // 2. If no pre-made SDF, load raw TTF and convert at runtime
            Font rawFont = GetFont(name);
            if (rawFont != null) {
                TMP_FontAsset dynamicSdf = TMP_FontAsset.CreateFontAsset(rawFont);
                dynamicSdf.name = name + " Runtime SDF";
                _tmpFontCache[name] = dynamicSdf;
                return dynamicSdf;
            }"""

new_logic = """            // 2. If no pre-made SDF, load raw TTF and convert at runtime
            Font rawFont = GetFont(name);
            if (rawFont != null) {
                TMP_FontAsset dynamicSdf = TMP_FontAsset.CreateFontAsset(rawFont);
                dynamicSdf.name = name + " Runtime SDF";
                
                // Add fallback for missing characters (like Japanese quotes 「 」)
                if (dynamicSdf.fallbackFontAssetTable == null)
                    dynamicSdf.fallbackFontAssetTable = new System.Collections.Generic.List<TMP_FontAsset>();
                
                TMP_FontAsset fallback = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
                if (fallback != null) dynamicSdf.fallbackFontAssetTable.Add(fallback);
                
                _tmpFontCache[name] = dynamicSdf;
                return dynamicSdf;
            }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Success")
else:
    print("Pattern not found")
