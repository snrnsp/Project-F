import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the text speed block
start_marker = "float yPos = -100;"
end_marker = "            // Preview Text & Background"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_block = '''float yPos = -100;

            // 〓〓〓 1. Text Speed 〓〓〓
            var textSpeedLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.text_speed", "텍스트 속도 조절"), yPos);
            Slider textSpeedSlider = CreateSettingsSlider(panel.transform, yPos);
            
            // REALLY FORCE COORDINATES
            RectTransform tsLabelRt = textSpeedLabel.GetComponent<RectTransform>();
            tsLabelRt.anchoredPosition = new Vector2(-160, yPos);
            tsLabelRt.sizeDelta = new Vector2(280, 40);
            tsLabelRt.pivot = new Vector2(0.5f, 1f);
            
            RectTransform tsSliderRt = textSpeedSlider.GetComponent<RectTransform>();
            tsSliderRt.anchoredPosition = new Vector2(100, yPos);
            tsSliderRt.sizeDelta = new Vector2(240, 20);
            tsSliderRt.pivot = new Vector2(0.5f, 1f);

'''
    content = content[:start_idx] + new_block + content[end_idx:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Text Speed label text to '텍스트 속도 조절'.")
