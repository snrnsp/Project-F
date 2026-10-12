import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Skip
content = content.replace('var skipTuple = CreateLegacyButton(skipRow.transform, "Ctrl ▼", 240, 40, new Color32(60, 40, 80, 255));',
                          'var skipTuple = CreateLegacyButton(skipRow.transform, "Ctrl ▼", 350, 40, new Color32(60, 40, 80, 255));')

# Font
content = content.replace('var fontTuple = CreateLegacyButton(fontRow.transform, Loc.Get("ui.settings.font_handwriting", "손글씨"), 240, 40, new Color32(60, 40, 80, 255));',
                          'var fontTuple = CreateLegacyButton(fontRow.transform, Loc.Get("ui.settings.font_handwriting", "손글씨"), 350, 40, new Color32(60, 40, 80, 255));')

# Flash
content = content.replace('var flashTuple = CreateLegacyButton(flashRow.transform, Loc.Get("ui.settings.flash_on", "켜짐"), 240, 40, new Color32(60, 40, 80, 255));',
                          'var flashTuple = CreateLegacyButton(flashRow.transform, Loc.Get("ui.settings.flash_on", "켜짐"), 350, 40, new Color32(60, 40, 80, 255));')

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Updated button widths to 350.")
