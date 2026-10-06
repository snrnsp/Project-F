import re

with open('Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

new_font_block = '''        private void EnsureGlobalFontsLoaded()
        {
            if (hwFontAsset != null) return;
            string primaryFontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(SettingsData.Language);
            hwFontAsset = HalloweenVN.UI.FontHelper.GetTMPFont(primaryFontName);
        }'''

content = re.sub(r'        private void EnsureGlobalFontsLoaded\(\)\s*\{.*?\}\s*\}', new_font_block, content, flags=re.DOTALL)

with open('Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("Patched HalloweenUIBuilder.cs correctly")
