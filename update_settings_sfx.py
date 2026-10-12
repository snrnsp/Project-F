import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''        private void OnSFXVolumeChanged(float value)
        {
            SettingsData.SFXVolume = value;
            if (AudioManager.Instance != null)
            {
                AudioManager.Instance.UpdateVolume();
                // Audible preview so the player can hear the new SFX level while dragging.
                if (Time.unscaledTime - lastSfxPreviewTime > 0.15f)
                {
                    lastSfxPreviewTime = Time.unscaledTime;
                    AudioManager.Instance.PlaySFX("sfx_ui_click");
                }
            }
            UpdateVolumeTexts();
        }'''

new_code = '''        private void OnSFXVolumeChanged(float value)
        {
            SettingsData.SFXVolume = value;
            if (AudioManager.Instance != null)
            {
                AudioManager.Instance.UpdateVolume();
            }
            UpdateVolumeTexts();
        }'''

content = content.replace(old_code, new_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated SettingsUI.cs to remove continuous click on slider drag.")
