import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace UIHelper.AddText for LanguageUI Title
target_title = 'UIHelper.AddText(titleObj, "언어 설정", HalloweenTheme.AccentOrange, 28, TextAlignmentOptions.Center);'
replacement_title = 'CreateLegacyText(titleObj, "언어 설정", HalloweenTheme.AccentOrange, 28, TextAnchor.MiddleCenter);'
text = text.replace(target_title, replacement_title)

# Replace Language Buttons
target_buttons = '''            string[] labels = { "한국어", "English", "日本語", "简体中文", "繁體中文" };
            Button[] btns = new Button[labels.Length];
            for (int i = 0; i < labels.Length; i++)
            {
                var btnTuple = UIHelper.CreateButton(langContainer.transform, labels[i], 300, 45, new Color32(40, 25, 60, 255));
                btns[i] = btnTuple.btn;
            }'''

replacement_buttons = '''            string[] labels = { "한국어", "English", "日本語", "简体中文", "繁體中文" };
            Button[] btns = new Button[labels.Length];
            for (int i = 0; i < labels.Length; i++)
            {
                var btnTuple = CreateLegacyButton(langContainer.transform, labels[i], 300, 45, new Color32(40, 25, 60, 255));
                btns[i] = btnTuple.btn;
            }'''

text = text.replace(target_buttons, replacement_buttons)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated LanguageUI to use LegacyText and Arial.ttf for CJK fallback')
