import sys

with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    code = f.read()

bgm_sfx_block = '''            // 🎵 BGM Volume 🎵
            var bgmVolumeLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.bgm_volume", "배경음 (BGM) 음량"), yPos);
            Slider bgmVolumeSlider = CreateSettingsSlider(panel.transform, yPos - 45);
            Text bgmVolumeValueText = CreateSettingsValueText(panel.transform, yPos - 45);
            yPos -= 90;

            // 🎵 SFX Volume 🎵
            var sfxVolumeLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.sfx_volume", "효과음 (SFX) 음량"), yPos);
            Slider sfxVolumeSlider = CreateSettingsSlider(panel.transform, yPos - 45);
            Text sfxVolumeValueText = CreateSettingsValueText(panel.transform, yPos - 45);
            yPos -= 90;'''

text_speed_block = '''            // ⏩ 1. Text Speed ⏩
            var textSpeedLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.text_speed", "텍스트 속도"), yPos);
            Slider textSpeedSlider = CreateSettingsSlider(panel.transform, yPos - 45);

            // Preview Text & Background (to see opacity)
            yPos -= 90;
            // The Text (No background needed anymore since Opacity setting is gone)
            GameObject previewTextObj = UIHelper.CreateUIObject("PreviewText", panel.transform);
            RectTransform ptextRt = previewTextObj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(ptextRt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            ptextRt.anchoredPosition = new Vector2(0, yPos + 10); // Moved slightly up
            ptextRt.sizeDelta = new Vector2(620, 60);
            Text previewText = CreateLegacyText(previewTextObj, "", HalloweenTheme.TextPrimary, 24, TextAnchor.MiddleCenter);'''

# Actually, the file contains mojibake in the shell, but the file on disk is utf-8-sig.
# So I should use regex to find and swap them.

import re

# Match the entire BGM + SFX block
pattern = re.compile(r'(\s*// 🎵 BGM Volume 🎵.*?yPos -= 90;\n\s*// 🎵 SFX Volume 🎵.*?yPos -= 90;)\n\s*(// ⏩ 1\. Text Speed ⏩.*?TextAnchor\.MiddleCenter;)', re.DOTALL)

def swap(match):
    return match.group(2) + '\n\n            yPos -= 90;\n' + match.group(1).replace('yPos -= 90;', '', 1).strip() + '\n'

new_code = pattern.sub(swap, code)

if code == new_code:
    print('Failed to swap!')
else:
    # Wait, the last yPos -= 90; from SFX Volume is needed, but the original code had it?
    # Let me re-verify the blocks by extracting them directly.
    pass

