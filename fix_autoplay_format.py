import sys

path = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Restore 0.1 rounding
content = content.replace(
    'SettingsData.AutoPlayDelay = Mathf.Round(val * 2f) / 2f;',
    'SettingsData.AutoPlayDelay = Mathf.Round(val * 10f) / 10f;'
)

# Restore 2.0 format, but without the confusing 's'
old_format = """
            if (autoPlayValueText != null)
                float apd = SettingsData.AutoPlayDelay;
                if (apd == Mathf.Floor(apd))
                    autoPlayValueText.text = ((int)apd).ToString() + "s";
                else
                    autoPlayValueText.text = apd.ToString("0.#") + "s";
"""
new_format = """
            if (autoPlayValueText != null)
                autoPlayValueText.text = SettingsData.AutoPlayDelay.ToString("0.0");
"""

# Try to find exactly how it's formatted
if 'float apd = SettingsData.AutoPlayDelay;' in content:
    lines = content.split('\n')
    new_lines = []
    skip = False
    for line in lines:
        if 'if (autoPlayValueText != null)' in line:
            # We are at the block.
            new_lines.append('            if (autoPlayValueText != null)')
            new_lines.append('                autoPlayValueText.text = SettingsData.AutoPlayDelay.ToString("0.0");')
            skip = True
            continue
        if skip:
            if 'if (skipModeValueText != null)' in line:
                skip = False
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    content = '\n'.join(new_lines)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("SettingsUI.cs updated")
