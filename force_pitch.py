import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/AudioManager.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = '''                if (sfxName.StartsWith("sfx_ui_"))
                {
                    uiSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
                }'''

new_code = '''                if (sfxName.StartsWith("sfx_ui_"))
                {
                    uiSource.pitch = 2.0f;
                    uiSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
                }'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Forced uiSource pitch in PlaySFX.")
else:
    print("Could not find the target code string.")
