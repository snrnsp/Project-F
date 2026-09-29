import sys

path = 'F:/Project-F/Assets/Scripts/UI/FontHelper.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_logic_1 = """            // 1. Try to load pre-made SDF asset
            TMP_FontAsset sdf = Resources.Load<TMP_FontAsset>("Fonts/" + name + " SDF");
            if (sdf != null) {
                _tmpFontCache[name] = sdf;
                return sdf;
            }"""

new_logic_1 = """            // 1. Try to load pre-made SDF asset
            TMP_FontAsset sdf = Resources.Load<TMP_FontAsset>("Fonts/" + name + " SDF");
            if (sdf != null) {
                // Ensure fallback exists even for pre-made SDFs
                if (name != "MalgunGothic") {
                    if (sdf.fallbackFontAssetTable == null)
                        sdf.fallbackFontAssetTable = new System.Collections.Generic.List<TMP_FontAsset>();
                    
                    bool hasFallback = false;
                    foreach (var fb in sdf.fallbackFontAssetTable) {
                        if (fb != null && fb.name.Contains("MalgunGothic")) {
                            hasFallback = true;
                            break;
                        }
                    }
                    
                    if (!hasFallback) {
                        TMP_FontAsset fallback = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
                        if (fallback != null) sdf.fallbackFontAssetTable.Add(fallback);
                    }
                }
                
                _tmpFontCache[name] = sdf;
                return sdf;
            }"""

if old_logic_1 in content:
    content = content.replace(old_logic_1, new_logic_1)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("FontHelper.cs pre-made SDF fallback updated")
else:
    print("Pattern not found for pre-made SDF")
