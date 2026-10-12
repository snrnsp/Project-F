import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/AudioManager.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = '''                if (sfxName.StartsWith("sfx_ui_"))
                {
                    uiSource.pitch = 2.0f;
                    uiSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
                }'''

new_code = '''                if (sfxName.StartsWith("sfx_ui_"))
                {
                    // Force a dedicated AudioSource to guarantee pitch changes apply on all platforms
                    GameObject tempAudio = new GameObject("TempUI_" + sfxName);
                    tempAudio.transform.SetParent(this.transform);
                    AudioSource tempSource = tempAudio.AddComponent<AudioSource>();
                    tempSource.clip = clip;
                    tempSource.volume = SettingsData.SFXVolume * gain;
                    tempSource.pitch = 2.0f;
                    tempSource.spatialBlend = 0f;
                    tempSource.Play();
                    Destroy(tempAudio, clip.length / 2.0f + 0.1f);
                }'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Replaced UI sound logic with dedicated temp AudioSource.")
else:
    print("Could not find the target code string.")
