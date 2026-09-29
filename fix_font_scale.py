import sys

path = 'F:/Project-F/Assets/Scripts/UI/FontHelper.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

injection_point = "                _tmpFontCache[name] = sdf;\n                return sdf;"

new_logic = """                // Adjust scales for notoriously large fonts
                if (name == "ZenKurenaido-Regular" || name == "MaShanZheng-Regular") {
                    var info = sdf.faceInfo;
                    // Japanese handwriting font is naturally huge, scale it down to match others
                    info.scale = name == "ZenKurenaido-Regular" ? 0.75f : 0.8f; 
                    sdf.faceInfo = info;
                }

                _tmpFontCache[name] = sdf;
                return sdf;"""

if 'Adjust scales for notoriously large fonts' not in content:
    content = content.replace(injection_point, new_logic)
    
    # Also inject it for dynamically created SDFs just in case
    injection_point2 = "            _tmpFontCache[name] = dynamicSdf;\n            return dynamicSdf;"
    new_logic2 = """            if (name == "ZenKurenaido-Regular" || name == "MaShanZheng-Regular") {
                var info = dynamicSdf.faceInfo;
                info.scale = name == "ZenKurenaido-Regular" ? 0.75f : 0.8f;
                dynamicSdf.faceInfo = info;
            }
            
            _tmpFontCache[name] = dynamicSdf;
            return dynamicSdf;"""
    content = content.replace(injection_point2, new_logic2)

    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Font scale logic injected")
else:
    print("Already injected")
