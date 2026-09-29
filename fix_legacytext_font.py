import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_legacy_text = """        private Text CreateLegacyText(GameObject parentObj, string label, Color32 color, int fontSize, TextAnchor alignment)
        {
            Text legacyText = parentObj.AddComponent<Text>();
            legacyText.text = label;
            legacyText.fontSize = fontSize;
            legacyText.alignment = alignment;
            legacyText.alignByGeometry = true;
            legacyText.verticalOverflow = VerticalWrapMode.Overflow;
            legacyText.color = color;

            // Load MalgunGothic TTF from Resources to ensure CJK characters render in WebGL
            // OS Fonts are not accessible in WebGL.
            Font rawFont = Resources.Load<Font>("Fonts/MalgunGothic");
            if (rawFont != null) legacyText.font = rawFont;
            else legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");

            return legacyText;
        }"""

new_legacy_text = """        private Text CreateLegacyText(GameObject parentObj, string label, Color32 color, int fontSize, TextAnchor alignment)
        {
            Text legacyText = parentObj.AddComponent<Text>();
            legacyText.text = label;
            legacyText.fontSize = fontSize;
            legacyText.alignment = alignment;
            legacyText.alignByGeometry = true;
            legacyText.verticalOverflow = VerticalWrapMode.Overflow;
            legacyText.color = color;

            string fontName = FontHelper.GetFontNameForLanguage(SettingsData.Language);
            Font f = FontHelper.GetFont(fontName);
            if (f != null) {
                legacyText.font = f;
            } else {
                Font rawFont = Resources.Load<Font>("Fonts/MalgunGothic");
                if (rawFont != null) legacyText.font = rawFont;
                else legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            }

            return legacyText;
        }"""

if old_legacy_text in content:
    content = content.replace(old_legacy_text, new_legacy_text)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Success")
else:
    print("Not found")
