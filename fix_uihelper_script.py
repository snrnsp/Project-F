import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/UIHelper.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'public static TextMeshProUGUI AddText' in line:
        start_idx = i
    if start_idx != -1 and 'return tmp;' in line:
        end_idx = i + 2
        break
        
if start_idx != -1 and end_idx != -1:
    new_method = """        public static TextMeshProUGUI AddText(GameObject obj, string text, Color color, float fontSize, TextAlignmentOptions alignment = TextAlignmentOptions.Left)
        {
            TextMeshProUGUI tmp = obj.AddComponent<TextMeshProUGUI>();
            tmp.text = text;
            tmp.color = color;
            tmp.fontSize = fontSize;
            tmp.alignment = alignment;

            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(HalloweenVN.Core.SettingsData.Language);
            TMP_FontAsset fontAsset = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            
            if (fontAsset != null)
            {
                tmp.font = fontAsset;
            }
            else
            {
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
        }\n"""
    
    lines = lines[:start_idx] + [new_method] + lines[end_idx:]
    
    with open(path, 'w', encoding='utf-8-sig') as fw:
        fw.writelines(lines)
    print("Success")
