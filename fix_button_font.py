import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_str = """            // Assign standard OS font to prevent Chinese characters from breaking
            Font rawFont = Resources.Load<Font>("Fonts/MalgunGothic");
            if (rawFont != null) legacyText.font = rawFont;
            else legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");"""

new_str = """            // Use proper localized font to ensure consistency
            string fontName = FontHelper.GetFontNameForLanguage(SettingsData.Language);
            Font f = FontHelper.GetFont(fontName);
            if (f != null) {
                legacyText.font = f;
            } else {
                Font rawFont = Resources.Load<Font>("Fonts/MalgunGothic");
                if (rawFont != null) legacyText.font = rawFont;
                else legacyText.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            }"""

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("✅ CreateLegacyButton 폰트 할당 로직 개선 완료")
else:
    print("❌ 대상 텍스트를 찾을 수 없습니다.")
