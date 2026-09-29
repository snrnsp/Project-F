import sys

path = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_logic = """    private void ApplyFontToAll(Font f)
    {
        if (titleTextLabel != null) titleTextLabel.font = f;
        if (textSpeedLabel != null) textSpeedLabel.font = f;
        if (autoPlayLabel != null) autoPlayLabel.font = f;
        if (autoPlayValueText != null)
            autoPlayValueText.text = SettingsData.AutoPlayDelay.ToString("0.0");
        if (skipModeValueText != null) skipModeValueText.font = f;
        if (fontStyleLabel != null) fontStyleLabel.font = f;
        if (fontStyleValueText != null) fontStyleValueText.font = f;
        if (closeButtonText != null) closeButtonText.font = f;
        if (previewTextLabel != null) previewTextLabel.font = f;
    }"""

new_logic = """    private void ApplyFontToAll(Font f)
    {
        if (titleTextLabel != null) titleTextLabel.font = f;
        if (textSpeedLabel != null) textSpeedLabel.font = f;
        if (autoPlayLabel != null) autoPlayLabel.font = f;
        if (autoPlayValueText != null) {
            autoPlayValueText.font = f;
            autoPlayValueText.text = SettingsData.AutoPlayDelay.ToString("0.0");
        }
        if (opacityLabel != null) opacityLabel.font = f;
        if (skipModeLabel != null) skipModeLabel.font = f;
        if (skipModeValueText != null) skipModeValueText.font = f;
        if (fontStyleLabel != null) fontStyleLabel.font = f;
        if (fontStyleValueText != null) fontStyleValueText.font = f;
        if (closeButtonText != null) closeButtonText.font = f;
        if (previewTextLabel != null) previewTextLabel.font = f;
    }"""

if 'if (opacityLabel != null) opacityLabel.font = f;' not in content:
    content = content.replace(old_logic, new_logic)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Fixed ApplyFontToAll missing labels")
else:
    print("Already fixed")
