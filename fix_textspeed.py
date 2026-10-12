import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We need to replace everything from loat yPos = -100; down to yPos -= 50; (Preview text)
start_marker = "float yPos = -100;"
end_marker = "            // Preview Text & Background"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find markers!")
    sys.exit(1)

new_block = '''float yPos = -100;

            // 〓〓〓 1. Text Speed 〓〓〓
            var textSpeedLabel = CreateSettingsLabel(panel.transform, Loc.Get("ui.settings.text_speed", "텍스트 속도"), yPos);
            Slider textSpeedSlider = CreateSettingsSlider(panel.transform, yPos);
            
            // FORCE coordinates just in case
            RectTransform tsLabelRt = textSpeedLabel.GetComponent<RectTransform>();
            tsLabelRt.anchoredPosition = new Vector2(-160, yPos);
            tsLabelRt.sizeDelta = new Vector2(280, 40);
            
            RectTransform tsSliderRt = textSpeedSlider.GetComponent<RectTransform>();
            tsSliderRt.anchoredPosition = new Vector2(100, yPos);
            tsSliderRt.sizeDelta = new Vector2(240, 20);

'''

content = content[:start_idx] + new_block + content[end_idx:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Forced Text Speed coordinates.")
