import sys
sys.stdout.reconfigure(encoding='utf-8')

path = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Add font update to UpdateLanguage()
old_str = """        public void UpdateLanguage()
        {

            if (skipButtonText != null) skipButtonText.resizeTextForBestFit = false;"""

new_str = """        public void UpdateLanguage()
        {
            var lang = HalloweenVN.Core.SettingsData.Language;
            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(lang);
            var f = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            if (f != null) {
                if (dialogueText != null) dialogueText.font = f;
                if (speakerNameText != null) speakerNameText.font = f;
                if (narratorText != null) narratorText.font = f;
            }
            
            var legacyF = HalloweenVN.UI.FontHelper.GetFont(fontName);
            if (legacyF != null) {
                if (skipButtonText != null) skipButtonText.font = legacyF;
                if (backlogButtonText != null) backlogButtonText.font = legacyF;
                if (autoButtonText != null) autoButtonText.font = legacyF;
            }

            if (skipButtonText != null) skipButtonText.resizeTextForBestFit = false;"""

if old_str in content:
    content = content.replace(old_str, new_str)
    
    # We also need to fix narratorText creation fallback just in case
    old_narrator = """        private void CreateNarratorText()
        {
            if (dialoguePanelRoot == null) return;
            
            GameObject textObj = new GameObject("NarratorText");
            textObj.transform.SetParent(dialoguePanelRoot.transform, false);
            
            RectTransform textRt = textObj.AddComponent<RectTransform>();
            textRt.anchorMin = Vector2.zero;
            textRt.anchorMax = Vector2.one;
            textRt.offsetMin = Vector2.zero;
            textRt.offsetMax = Vector2.zero;
            textRt.sizeDelta = Vector2.zero;

            narratorText = textObj.AddComponent<TextMeshProUGUI>();
            narratorText.margin = new Vector4(100, 100, 100, 100);

            TMP_FontAsset font = null;
            if (dialogueText != null && dialogueText.font != null)
                font = dialogueText.font;
            if (font == null)
                font = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
            if (font == null)
                font = TMP_Settings.defaultFontAsset;"""

    new_narrator = """        private void CreateNarratorText()
        {
            if (dialoguePanelRoot == null) return;
            
            GameObject textObj = new GameObject("NarratorText");
            textObj.transform.SetParent(dialoguePanelRoot.transform, false);
            
            RectTransform textRt = textObj.AddComponent<RectTransform>();
            textRt.anchorMin = Vector2.zero;
            textRt.anchorMax = Vector2.one;
            textRt.offsetMin = Vector2.zero;
            textRt.offsetMax = Vector2.zero;
            textRt.sizeDelta = Vector2.zero;

            narratorText = textObj.AddComponent<TextMeshProUGUI>();
            narratorText.margin = new Vector4(100, 100, 100, 100);

            TMP_FontAsset font = null;
            string fontName = HalloweenVN.UI.FontHelper.GetFontNameForLanguage(HalloweenVN.Core.SettingsData.Language);
            font = HalloweenVN.UI.FontHelper.GetTMPFont(fontName);
            
            if (font == null && dialogueText != null && dialogueText.font != null)
                font = dialogueText.font;
            if (font == null)
                font = Resources.Load<TMP_FontAsset>("Fonts/MalgunGothic SDF");
            if (font == null)
                font = TMP_Settings.defaultFontAsset;"""

    if old_narrator in content:
        content = content.replace(old_narrator, new_narrator)
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        print("✅ DialogueUI.cs 폰트 동기화 로직 적용 완료")
    else:
        print("❌ CreateNarratorText 부분을 찾지 못했습니다.")
else:
    print("❌ UpdateLanguage 부분을 찾지 못했습니다.")
