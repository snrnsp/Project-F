import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/AudioManager.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_playsfx = '''                if (sfxName.StartsWith("sfx_ui_"))
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
                    Debug.Log("[AudioManager] Played UI SFX at 2x pitch!");
                    Destroy(tempAudio, clip.length / 2.0f + 0.1f);
                }'''

new_playsfx = '''                if (sfxName.StartsWith("sfx_ui_"))
                {
                    uiSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
                }'''

if old_playsfx in content:
    content = content.replace(old_playsfx, new_playsfx)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Reverted PlaySFX back to PlayOneShot.")
else:
    print("Could not find the target code string.")
