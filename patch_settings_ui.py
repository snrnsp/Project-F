import re

with open('Assets/Scripts/UI/SettingsUI.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Add to OnEnable
onenable_old = '''            if (autoPlaySlider != null)
            {
                autoPlaySlider.minValue = 0.1f;
                autoPlaySlider.maxValue = 5f;
                autoPlaySlider.value = SettingsData.AutoPlayDelay;
                autoPlaySlider.onValueChanged.AddListener(OnAutoPlayChanged);
            }'''

onenable_new = '''            if (autoPlaySlider != null)
            {
                autoPlaySlider.minValue = 0.1f;
                autoPlaySlider.maxValue = 5f;
                autoPlaySlider.value = SettingsData.AutoPlayDelay;
                autoPlaySlider.onValueChanged.AddListener(OnAutoPlayChanged);
            }

            if (fullscreenToggle != null)
            {
                fullscreenToggle.isOn = SettingsData.EnableFlashingEffects;
                fullscreenToggle.onValueChanged.AddListener(OnEpilepsyToggled);
            }'''

if onenable_old in content:
    content = content.replace(onenable_old, onenable_new)
else:
    print("Could not find OnEnable block")

# Add OnEpilepsyToggled method
callbacks_old = '''        // --- Callbacks ---'''
callbacks_new = '''        // --- Callbacks ---
        
        private void OnEpilepsyToggled(bool value)
        {
            SettingsData.EnableFlashingEffects = value;
            SettingsData.Save();
            UpdateAllLabels();
        }'''

if callbacks_old in content:
    content = content.replace(callbacks_old, callbacks_new)
else:
    print("Could not find Callbacks block")


# Update label
update_labels_old = '''            if (ctrlSkipValueText != null)'''
update_labels_new = '''            if (fullscreenToggle != null)
            {
                Text t = fullscreenToggle.GetComponentInChildren<Text>();
                if (t != null)
                {
                    if (lang == GameLanguage.Korean) t.text = "광과민성 이펙트 허용";
                    else t.text = "Allow Flashing Effects";
                }
            }
            if (ctrlSkipValueText != null)'''

if update_labels_old in content:
    content = content.replace(update_labels_old, update_labels_new)
else:
    print("Could not find UpdateAllLabels block")

# Add to OnDisable
ondisable_old = '''            if (autoPlaySlider != null) autoPlaySlider.onValueChanged.RemoveListener(OnAutoPlayChanged);'''
ondisable_new = '''            if (autoPlaySlider != null) autoPlaySlider.onValueChanged.RemoveListener(OnAutoPlayChanged);
            if (fullscreenToggle != null) fullscreenToggle.onValueChanged.RemoveListener(OnEpilepsyToggled);'''

if ondisable_old in content:
    content = content.replace(ondisable_old, ondisable_new)
else:
    print("Could not find OnDisable block")

with open('Assets/Scripts/UI/SettingsUI.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Patched SettingsUI.cs")
