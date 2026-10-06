import re

with open('Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace the dynamic font creation
new_font_block = '''        private void EnsureGlobalFontsLoaded()
        {
            if (hwFontAsset != null) return;
            string primaryFontName = "MalgunGothic SDF"; // Just use the SDF font directly
            hwFontAsset = Resources.Load<TMP_FontAsset>("Fonts/" + primaryFontName);
        }'''

content = re.sub(r'        private void EnsureGlobalFontsLoaded\(\)\s*\{.*?\}\s*\}', new_font_block, content, flags=re.DOTALL)

with open('Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("Patched HalloweenUIBuilder.cs")
