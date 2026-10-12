import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add forceful repositioning at the end of UpdateAllLabels
force_code = '''
            if (textSpeedSlider != null) {
                RectTransform tsRt = textSpeedSlider.GetComponent<RectTransform>();
                tsRt.anchoredPosition = new Vector2(100, -100);
                tsRt.sizeDelta = new Vector2(240, 20);
                tsRt.pivot = new Vector2(0.5f, 1f);
                tsRt.anchorMin = new Vector2(0.5f, 1f);
                tsRt.anchorMax = new Vector2(0.5f, 1f);
            }
            if (textSpeedLabel != null) {
                RectTransform tlRt = textSpeedLabel.GetComponent<RectTransform>();
                tlRt.anchoredPosition = new Vector2(-160, -100);
                tlRt.sizeDelta = new Vector2(280, 40);
                tlRt.pivot = new Vector2(0.5f, 1f);
                tlRt.anchorMin = new Vector2(0.5f, 1f);
                tlRt.anchorMax = new Vector2(0.5f, 1f);
            }
'''

content = content.replace('if (flashEffectValueText != null) flashEffectValueText.text = SettingsData.EnableFlashingEffects ? Loc.Get("ui.settings.flash_on", "켜짐") : Loc.Get("ui.settings.flash_off", "꺼짐");', 
    'if (flashEffectValueText != null) flashEffectValueText.text = SettingsData.EnableFlashingEffects ? Loc.Get("ui.settings.flash_on", "켜짐") : Loc.Get("ui.settings.flash_off", "꺼짐");' + force_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Added forceful repositioning to SettingsUI.cs")
