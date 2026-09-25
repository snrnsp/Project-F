import codecs

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

bad_str = """            string[] fontNames = { 
                "Malgun Gothic", "Apple SD Gothic Neo", // Korean
                "Meiryo", "Yu Gothic", "MS Gothic", "Hiragino Sans", // Japanese
                "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC", // Simplified Chinese
                "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC", // Traditional Chinese
                "Arial Unicode MS", "sans-serif" // Fallbacks
            };
            Font rawFont = Font.CreateDynamicFontFromOSFont(fontNames, fontSize);
            if (rawFont != null) legacyText.font = rawFont;
            else legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");"""

good_str = """            // Load MalgunGothic TTF from Resources to ensure CJK characters render in WebGL
            // OS Fonts are not accessible in WebGL.
            Font rawFont = Resources.Load<Font>("Fonts/MalgunGothic");
            if (rawFont != null) legacyText.font = rawFont;
            else legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");"""

# Handle Windows line endings
bad_str_win = bad_str.replace('\n', '\r\n')

if bad_str_win in text:
    text = text.replace(bad_str_win, good_str)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Fixed CreateLegacyText fonts (Win LF)!")
else:
    # try without \r
    if bad_str in text:
        text = text.replace(bad_str, good_str)
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(text)
        print("Fixed CreateLegacyText fonts (LF mode)!")
    else:
        print("Could not find the target string.")
