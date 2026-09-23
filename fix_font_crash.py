import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            // Use standard Arial which Unity automatically links to OS fallbacks for CJK
            legacyText.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
            if (legacyText.font == null) legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");'''

replacement = '''            string[] fontNames = { 
                "Malgun Gothic", "Apple SD Gothic Neo", // Korean
                "Meiryo", "Yu Gothic", "MS Gothic", "Hiragino Sans", // Japanese
                "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC", // Simplified Chinese
                "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC", // Traditional Chinese
                "Arial Unicode MS", "sans-serif" // Fallbacks
            };
            Font rawFont = Font.CreateDynamicFontFromOSFont(fontNames, fontSize);
            if (rawFont != null) legacyText.font = rawFont;
            else legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Reverted Arial.ttf hack and added full CJK dynamic font support')
