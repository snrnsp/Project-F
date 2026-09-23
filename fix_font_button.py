import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Update CreateLegacyButton
target1 = '''            string[] fontNames = { "Malgun Gothic", "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC", "Arial Unicode MS" };
            Font rawFont = Font.CreateDynamicFontFromOSFont(fontNames, 20);'''

replacement1 = '''            string[] fontNames = { 
                "Malgun Gothic", "Apple SD Gothic Neo",
                "Meiryo", "Yu Gothic", "MS Gothic", "Hiragino Sans",
                "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC",
                "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC",
                "Arial Unicode MS", "sans-serif"
            };
            Font rawFont = Font.CreateDynamicFontFromOSFont(fontNames, 20);'''

# Note: The CreateLegacyText was already updated by the previous script, so I just need to update CreateLegacyButton.

text = text.replace(target1, replacement1)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated CreateLegacyButton font fallback list')
