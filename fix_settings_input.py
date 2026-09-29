import sys

path = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Replace declaration
content = content.replace('private Text autoPlayValueText;', 'private InputField autoPlayInputField;')

# Add to ApplyFontToAll
old_apply = """        if (autoPlayValueText != null) {
            autoPlayValueText.font = f;
            autoPlayValueText.text = SettingsData.AutoPlayDelay.ToString("0.0");
        }"""
new_apply = """        if (autoPlayInputField != null && autoPlayInputField.textComponent != null) {
            autoPlayInputField.textComponent.font = f;
            autoPlayInputField.text = SettingsData.AutoPlayDelay.ToString("0.0");
        }"""
content = content.replace(old_apply, new_apply)

# OnEnable - add listener
old_on_enable = """if (autoPlaySlider != null) autoPlaySlider.onValueChanged.AddListener(OnAutoPlayChanged);"""
new_on_enable = """if (autoPlaySlider != null) autoPlaySlider.onValueChanged.AddListener(OnAutoPlayChanged);
        if (autoPlayInputField != null) autoPlayInputField.onEndEdit.AddListener(OnAutoPlayInputEdit);"""
content = content.replace(old_on_enable, new_on_enable)

# OnDisable - remove listener
old_on_disable = """if (autoPlaySlider != null) autoPlaySlider.onValueChanged.RemoveListener(OnAutoPlayChanged);"""
new_on_disable = """if (autoPlaySlider != null) autoPlaySlider.onValueChanged.RemoveListener(OnAutoPlayChanged);
        if (autoPlayInputField != null) autoPlayInputField.onEndEdit.RemoveListener(OnAutoPlayInputEdit);"""
content = content.replace(old_on_disable, new_on_disable)

# Change OnAutoPlayChanged
old_on_changed = """        if (autoPlayValueText != null)
            autoPlayValueText.text = SettingsData.AutoPlayDelay.ToString("0.0");"""
new_on_changed = """        if (autoPlayInputField != null)
            autoPlayInputField.text = SettingsData.AutoPlayDelay.ToString("0.0");"""
content = content.replace(old_on_changed, new_on_changed)

# Add OnAutoPlayInputEdit method
method_to_add = """
    private void OnAutoPlayInputEdit(string val)
    {
        if (float.TryParse(val, out float result))
        {
            result = Mathf.Clamp(result, 0.1f, 5.0f);
            if (autoPlaySlider != null)
            {
                autoPlaySlider.value = result;
            }
            else
            {
                SettingsData.AutoPlayDelay = result;
                SettingsData.Save();
            }
            autoPlayInputField.text = result.ToString("0.0");
        }
        else
        {
            autoPlayInputField.text = SettingsData.AutoPlayDelay.ToString("0.0");
        }
    }
"""
content = content.replace('private void OnAutoPlayChanged(float val)', method_to_add + '\n    private void OnAutoPlayChanged(float val)')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("SettingsUI.cs updated for InputField")
