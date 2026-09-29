import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'private Text CreateLegacyText' in line:
        start_idx = i
    if start_idx != -1 and 'return legacyText;' in line:
        end_idx = i + 1
        break

if start_idx != -1 and end_idx != -1:
    new_method = """        private Text CreateLegacyText(GameObject parentObj, string label, Color32 color, int fontSize, TextAnchor alignment)
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
        }\n"""
    
    lines = lines[:start_idx] + [new_method] + lines[end_idx:]
    with open(path, 'w', encoding='utf-8-sig') as fw:
        fw.writelines(lines)
    print("Success")
