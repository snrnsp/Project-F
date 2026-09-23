import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '''msgText.font = Resources.GetBuiltinResource<Font>("Arial.ttf"); // Base font, will use OS fallbacks'''
rep1 = '''
            string[] fontNames = { 
                "Malgun Gothic", "Apple SD Gothic Neo",
                "Meiryo", "Yu Gothic", "MS Gothic", "Hiragino Sans",
                "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC",
                "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC",
                "Arial Unicode MS", "sans-serif"
            };
            Font cjkFont = Font.CreateDynamicFontFromOSFont(fontNames, 22);
            if (cjkFont == null) cjkFont = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            msgText.font = cjkFont;
'''

target2 = '''yesText.font = Resources.GetBuiltinResource<Font>("Arial.ttf");'''
rep2 = '''yesText.font = cjkFont;'''

target3 = '''noText.font = Resources.GetBuiltinResource<Font>("Arial.ttf");'''
rep3 = '''noText.font = cjkFont;'''

text = text.replace(target1, rep1).replace(target2, rep2).replace(target3, rep3)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Fixed font fallback in SettingsUI.cs popup')
