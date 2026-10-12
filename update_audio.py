import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/AudioManager.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add uiSource
content = content.replace('private AudioSource sfxSource;', 'private AudioSource sfxSource;\n        private AudioSource uiSource;')

init_old = '''            if (sfxSource == null)
            {
                sfxSource = gameObject.AddComponent<AudioSource>();
                sfxSource.loop = false;
                sfxSource.playOnAwake = false;
                sfxSource.spatialBlend = 0f;
            }
            // One-shots carry their own volume scale; keep the source at 1 so the'''
init_new = '''            if (sfxSource == null)
            {
                sfxSource = gameObject.AddComponent<AudioSource>();
                sfxSource.loop = false;
                sfxSource.playOnAwake = false;
                sfxSource.spatialBlend = 0f;
            }
            if (uiSource == null)
            {
                uiSource = gameObject.AddComponent<AudioSource>();
                uiSource.loop = false;
                uiSource.playOnAwake = false;
                uiSource.spatialBlend = 0f;
                uiSource.pitch = 2.0f; // Double speed for UI sounds
            }
            // One-shots carry their own volume scale; keep the source at 1 so the'''
content = content.replace(init_old, init_new)

# Update volume
vol_old = '''            if (sfxSource != null)
            {
                // SFX source is kept at 1, volume is applied per PlayOneShot.
                // Any looping/timed SFX coroutines handle their own volume.
            }'''
vol_new = '''            if (sfxSource != null)
            {
                // SFX source is kept at 1, volume is applied per PlayOneShot.
            }
            if (uiSource != null)
            {
                uiSource.volume = 1f;
            }'''
content = content.replace(vol_old, vol_new)

# Update PlaySFX
play_old = '''            if (maxDuration > 0f || offset > 0f)
            {
                PlayTimedSFX(sfxName, clip, gain, offset, maxDuration, fadeOutTime);
            }
            else
            {
                sfxSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
            }'''
play_new = '''            if (maxDuration > 0f || offset > 0f)
            {
                PlayTimedSFX(sfxName, clip, gain, offset, maxDuration, fadeOutTime);
            }
            else
            {
                if (sfxName.StartsWith("sfx_ui_"))
                {
                    uiSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
                }
                else
                {
                    sfxSource.PlayOneShot(clip, SettingsData.SFXVolume * gain);
                }
            }'''
content = content.replace(play_old, play_new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated AudioManager.cs with double speed uiSource")
