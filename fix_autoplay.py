import sys

# Fix 1: SettingsUI.cs - min value and rounding
path = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Change min from 1f to 0.1f and add wholeNumbers=false
content = content.replace(
    'autoPlaySlider.minValue = 1f;',
    'autoPlaySlider.minValue = 0.1f;'
)

# Fix rounding to 0.1 increments cleanly
content = content.replace(
    'SettingsData.AutoPlayDelay = Mathf.Round(val * 10f) / 10f;',
    'SettingsData.AutoPlayDelay = Mathf.Round(val * 2f) / 2f;'
)

# Fix display format - show "1s" for whole, "0.5s" for half, "0.1s" for 0.1
old_format = 'autoPlayValueText.text = SettingsData.AutoPlayDelay.ToString("0.0") + "s";'
new_format = '''float apd = SettingsData.AutoPlayDelay;
                if (apd == Mathf.Floor(apd))
                    autoPlayValueText.text = ((int)apd).ToString() + "s";
                else
                    autoPlayValueText.text = apd.ToString("0.#") + "s";'''
content = content.replace(old_format, new_format)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("1 SettingsUI fixed")

# Fix 2: SettingsData.cs - clamp min from 1.0 to 0.1
path2 = 'F:/Project-F/Assets/Scripts/Core/SettingsData.cs'
with open(path2, 'r', encoding='utf-8-sig') as f:
    content2 = f.read()

content2 = content2.replace(
    'Mathf.Clamp(AutoPlayDelay, 1.0f, 5.0f)',
    'Mathf.Clamp(AutoPlayDelay, 0.1f, 5.0f)'
)

with open(path2, 'w', encoding='utf-8-sig') as f:
    f.write(content2)
print("2 SettingsData fixed")

# Fix 3: HalloweenUIBuilder.cs - move value text closer
path3 = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path3, 'r', encoding='utf-8-sig') as f:
    content3 = f.read()

# Move value text from x=200 to x=130 (closer to label)
content3 = content3.replace(
    'autoValRt.anchoredPosition = new Vector2(200, yPos);',
    'autoValRt.anchoredPosition = new Vector2(130, yPos);'
)

with open(path3, 'w', encoding='utf-8-sig') as f:
    f.write(content3)
print("3 HalloweenUIBuilder fixed")
