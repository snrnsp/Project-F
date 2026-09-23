import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            string[] fontNames = { "Malgun Gothic", "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC", "Arial Unicode MS" };
            Font rawFont = Font.CreateDynamicFontFromOSFont(fontNames, fontSize);
            if (rawFont != null) legacyText.font = rawFont;
            else legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");'''

replacement = '''            // Use standard Arial which Unity automatically links to OS fallbacks for CJK
            legacyText.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
            if (legacyText.font == null) legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Updated LegacyText to use Arial.ttf for CJK fallback')
else:
    print('Target not found in HalloweenUIBuilder')
