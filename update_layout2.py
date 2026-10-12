import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace assignments one by one to ensure exact matching and positioning.

old_block_1 = '''            float yPos = -135;

            // 〓〓〓 1. Text Speed 〓〓〓
            var textSpeedLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.text_speed", "텍스트 속도"), yPos);
            Slider textSpeedSlider = CreateSettingsSlider(panel.transform, yPos - 45);'''

new_block_1 = '''            float yPos = -110;

            // 〓〓〓 1. Text Speed 〓〓〓
            var textSpeedLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.text_speed", "텍스트 속도"), yPos);
            Slider textSpeedSlider = CreateSettingsSlider(panel.transform, yPos);'''


old_block_2 = '''            // Preview Text & Background (to see opacity)
            yPos -= 90;
            // The Text (No background needed anymore since Opacity setting is gone)
            GameObject previewTextObj = UIHelper.CreateUIObject("PreviewText", panel.transform);
            RectTransform ptextRt = previewTextObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(ptextRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            ptextRt.anchoredPosition = new Vector2(0, yPos + 10); // Moved slightly up
            ptextRt.sizeDelta = new Vector2(620, 60);'''

new_block_2 = '''            // Preview Text & Background (to see opacity)
            yPos -= 60;
            // The Text (No background needed anymore since Opacity setting is gone)
            GameObject previewTextObj = UIHelper.CreateUIObject("PreviewText", panel.transform);
            RectTransform ptextRt = previewTextObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(ptextRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            ptextRt.anchoredPosition = new Vector2(0, yPos);
            ptextRt.sizeDelta = new Vector2(620, 60);'''

old_block_3 = '''            yPos -= 90;

            // 〓〓〓 BGM Volume 〓〓〓
            var bgmVolumeLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.bgm_volume", "배경음악 (BGM) 음량"), yPos);
            Slider bgmVolumeSlider = CreateSettingsSlider(panel.transform, yPos - 45);
            Text bgmVolumeValueText = CreateSettingsValueText(panel.transform, yPos - 45);
            yPos -= 90;

            // 〓〓〓 SFX Volume 〓〓〓
            var sfxVolumeLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.sfx_volume", "효과음 (SFX) 음량"), yPos);
            Slider sfxVolumeSlider = CreateSettingsSlider(panel.transform, yPos - 45);
            Text sfxVolumeValueText = CreateSettingsValueText(panel.transform, yPos - 45);

            // 〓〓〓 2. Auto-play Delay 〓〓〓
            yPos -= 95;
            var autoPlayLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.auto_play_delay", "오토 대기 시간"), yPos);
            Slider autoPlaySlider = CreateSettingsSlider(panel.transform, yPos - 45);

            // Value InputField (right side of slider)
            GameObject autoValObj = UIHelper.CreateUIObject("AutoPlayValue", panel.transform);
            RectTransform autoValRt = autoValObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(autoValRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            autoValRt.anchoredPosition = new Vector2(235, yPos - 40);'''

new_block_3 = '''            yPos -= 65;

            // 〓〓〓 BGM Volume 〓〓〓
            var bgmVolumeLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.bgm_volume", "배경음악 (BGM) 음량"), yPos);
            Slider bgmVolumeSlider = CreateSettingsSlider(panel.transform, yPos);
            Text bgmVolumeValueText = CreateSettingsValueText(panel.transform, yPos);
            
            yPos -= 65;

            // 〓〓〓 SFX Volume 〓〓〓
            var sfxVolumeLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.sfx_volume", "효과음 (SFX) 음량"), yPos);
            Slider sfxVolumeSlider = CreateSettingsSlider(panel.transform, yPos);
            Text sfxVolumeValueText = CreateSettingsValueText(panel.transform, yPos);

            // 〓〓〓 2. Auto-play Delay 〓〓〓
            yPos -= 65;
            var autoPlayLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.auto_play_delay", "오토 대기 시간"), yPos);
            Slider autoPlaySlider = CreateSettingsSlider(panel.transform, yPos);

            // Value InputField (right side of slider)
            GameObject autoValObj = UIHelper.CreateUIObject("AutoPlayValue", panel.transform);
            RectTransform autoValRt = autoValObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(autoValRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            autoValRt.anchoredPosition = new Vector2(260, yPos + 5);'''


content = content.replace(old_block_1, new_block_1)
content = content.replace(old_block_2, new_block_2)
content = content.replace(old_block_3, new_block_3)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated first half layout.")
