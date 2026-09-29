import sys

path = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_str = """            TMP_FontAsset font = null;
            if (dialogueText != null && dialogueText.font != null)
                font = dialogueText.font;
            if (font == null)
                font = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
            if (font == null)
                font = TMP_Settings.defaultFontAsset;"""

new_str = """            TMP_FontAsset font = null;
            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(HalloweenVN.Core.SettingsData.Language);
            font = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            
            if (font == null && dialogueText != null && dialogueText.font != null)
                font = dialogueText.font;
            if (font == null)
                font = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
            if (font == null)
                font = TMP_Settings.defaultFontAsset;"""

if old_str in content:
    content = content.replace(old_str, new_str)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("✅ DialogueUI.cs narratorText 폰트 로직 수정 완료")
else:
    print("❌ 대상 텍스트를 찾을 수 없습니다. (DialogueUI.cs)")
