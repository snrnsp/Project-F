import sys
import re

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# 1. Update BGM/SFX Value Text X position and width
old_val_text = '''        private Text CreateSettingsValueText(Transform parent, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject("VolumeValue", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(235, yPos + 3); // Visual alignment offset
            rt.sizeDelta = new Vector2(90, 30);'''
new_val_text = '''        private Text CreateSettingsValueText(Transform parent, float yPos)
        {
            GameObject obj = UIHelper.CreateUIObject("VolumeValue", parent);
            RectTransform rt = obj.GetComponent<RectTransform>();
            UIHelper.SetAnchors(rt, new Vector2(0.5f, 1), new Vector2(0.5f, 1), new Vector2(0.5f, 1));
            rt.anchoredPosition = new Vector2(310, yPos + 3); // Center at 310
            rt.sizeDelta = new Vector2(70, 30); // Width 70 (275 to 345)'''
if old_val_text in content:
    content = content.replace(old_val_text, new_val_text)
else:
    # Let's try with 300, 3
    old_val_text2 = old_val_text.replace('235', '300')
    if old_val_text2 in content:
        content = content.replace(old_val_text2, new_val_text)
    else:
        print("Could not find CreateSettingsValueText!")

# 2. Update BGM/SFX manual overwrites (if they exist) from 300, 3 to 310, 3
content = content.replace('anchoredPosition = new Vector2(300, 3);', 'anchoredPosition = new Vector2(310, 3);')

# 3. Update buttons from 350 width and 100 X to 420 width and 135 X
# Skip Mode
content = content.replace('var skipTuple = CreateLegacyButton(skipRow.transform, "Ctrl ▼", 350, 40', 'var skipTuple = CreateLegacyButton(skipRow.transform, "Ctrl ▼", 420, 40')
content = content.replace('skipTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(100, 0);', 'skipTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(135, 0);')

# Font Style
content = content.replace('var fontTuple = CreateLegacyButton(fontRow.transform, Loc.Get("ui.settings.font_handwriting", "손글씨"), 350, 40', 'var fontTuple = CreateLegacyButton(fontRow.transform, Loc.Get("ui.settings.font_handwriting", "손글씨"), 420, 40')
content = content.replace('fontTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(100, 0);', 'fontTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(135, 0);')

# Flash Effect
content = content.replace('var flashTuple = CreateLegacyButton(flashRow.transform, Loc.Get("ui.settings.flash_on", "켜짐"), 350, 40', 'var flashTuple = CreateLegacyButton(flashRow.transform, Loc.Get("ui.settings.flash_on", "켜짐"), 420, 40')
content = content.replace('flashTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(100, 0);', 'flashTuple.btn.GetComponent<RectTransform>().anchoredPosition = new Vector2(135, 0);')

# Dropdown panel and items
content = content.replace('dropRt.sizeDelta = new Vector2(350, 120);', 'dropRt.sizeDelta = new Vector2(420, 120);')
content = content.replace('dropRt.anchoredPosition = new Vector2(100, 10);', 'dropRt.anchoredPosition = new Vector2(135, 10);')
content = content.replace('CreateLegacyButton(dropPanelObj.transform, "Ctrl", 350, 40', 'CreateLegacyButton(dropPanelObj.transform, "Ctrl", 420, 40')
content = content.replace('CreateLegacyButton(dropPanelObj.transform, "Shift", 350, 40', 'CreateLegacyButton(dropPanelObj.transform, "Shift", 420, 40')
content = content.replace('CreateLegacyButton(dropPanelObj.transform, "Space", 350, 40', 'CreateLegacyButton(dropPanelObj.transform, "Space", 420, 40')

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Updated grid layout.")
