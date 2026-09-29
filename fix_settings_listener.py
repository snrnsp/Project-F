import sys

path = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_logic = """        if (autoPlaySlider != null)
        {
            autoPlaySlider.minValue = 0.1f;
            autoPlaySlider.maxValue = 5f;
            autoPlaySlider.value = SettingsData.AutoPlayDelay;
            autoPlaySlider.onValueChanged.AddListener(OnAutoPlayChanged);
        }"""
new_logic = """        if (autoPlaySlider != null)
        {
            autoPlaySlider.minValue = 0.1f;
            autoPlaySlider.maxValue = 5f;
            autoPlaySlider.value = SettingsData.AutoPlayDelay;
            autoPlaySlider.onValueChanged.AddListener(OnAutoPlayChanged);
        }
        if (autoPlayInputField != null)
        {
            autoPlayInputField.onEndEdit.AddListener(OnAutoPlayInputEdit);
        }"""

content = content.replace(old_logic, new_logic)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("SettingsUI OnEnable fixed")
