import sys
sys.stdout.reconfigure(encoding='utf-8')

path = 'F:/Project-F/Assets/Scripts/UI/Theme/UIHelper.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_addtext = """        public static TextMeshProUGUI AddText(GameObject obj, string text, Color color, float fontSize, TextAlignmentOptions alignment = TextAlignmentOptions.Left)
        {
            TextMeshProUGUI tmp = obj.AddComponent<TextMeshProUGUI>();
            tmp.text = text;
            tmp.color = color;
            tmp.fontSize = fontSize;
            tmp.alignment = alignment;

            // Load or create Korean Font at runtime
            if (cachedKoreanFont == null)
            {
                // Try to load pre-made asset first
                cachedKoreanFont = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");

                // If not found, create dynamic font asset from TTF at runtime
                if (cachedKoreanFont == null)
                {
                    Font rawFont = Resources.Load<Font>("Fonts/MalgunGothic");
                    if (rawFont != null)
                    {
                        cachedKoreanFont = TMP_FontAsset.CreateFontAsset(rawFont);
                        cachedKoreanFont.name = "MalgunGothic Runtime SDF";
                    }
                }
            }

            if (cachedKoreanFont != null)
            {
                tmp.font = cachedKoreanFont;
            }

            return tmp;
        }"""

new_addtext = """        public static TextMeshProUGUI AddText(GameObject obj, string text, Color color, float fontSize, TextAlignmentOptions alignment = TextAlignmentOptions.Left)
        {
            TextMeshProUGUI tmp = obj.AddComponent<TextMeshProUGUI>();
            tmp.text = text;
            tmp.color = color;
            tmp.fontSize = fontSize;
            tmp.alignment = alignment;

            // Use the globally selected language font and dynamically create SDF if needed
            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(HalloweenVN.Core.SettingsData.Language);
            TMP_FontAsset fontAsset = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            
            if (fontAsset != null)
            {
                tmp.font = fontAsset;
            }
            else
            {
                // Fallback to MalgunGothic
                if (cachedKoreanFont == null)
                {
                    cachedKoreanFont = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
                    if (cachedKoreanFont == null)
                    {
                        Font rawFont = Resources.Load<Font>("Fonts/MalgunGothic");
                        if (rawFont != null)
                        {
                            cachedKoreanFont = TMP_FontAsset.CreateFontAsset(rawFont);
                            cachedKoreanFont.name = "MalgunGothic Runtime SDF";
                        }
                    }
                }
                if (cachedKoreanFont != null) tmp.font = cachedKoreanFont;
            }

            return tmp;
        }"""

if old_addtext in content:
    content = content.replace(old_addtext, new_addtext)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("✅ UIHelper.cs 폰트 할당 로직 개선 완료")
else:
    print("❌ 대상 텍스트를 찾을 수 없습니다. (UIHelper)")
