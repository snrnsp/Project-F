import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/AudioManager.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_load = '''        private AudioClip LoadSFX(string sfxName)
        {
            if (string.IsNullOrEmpty(sfxName)) return null;
            if (sfxCache.TryGetValue(sfxName, out AudioClip clip)) return clip;
            clip = Resources.Load<AudioClip>($"Audio/SFX/{sfxName}");
            if (clip != null) sfxCache[sfxName] = clip;
            else Debug.LogWarning($"[AudioManager] SFX not found: Audio/SFX/{sfxName}");
            return clip;
        }'''

new_load = '''        private AudioClip LoadSFX(string sfxName)
        {
            if (string.IsNullOrEmpty(sfxName)) return null;
            if (sfxCache.TryGetValue(sfxName, out AudioClip clip)) return clip;
            clip = Resources.Load<AudioClip>($"Audio/SFX/{sfxName}");
            
            if (clip != null) 
            {
                if (sfxName.StartsWith("sfx_ui_"))
                {
                    // Create a 2x sped-up version in memory by doubling the sample rate!
                    float[] data = new float[clip.samples * clip.channels];
                    clip.GetData(data, 0);
                    AudioClip fastClip = AudioClip.Create(clip.name + "_fast", clip.samples, clip.channels, (int)(clip.frequency * 2.0f), false);
                    fastClip.SetData(data, 0);
                    clip = fastClip;
                }
                sfxCache[sfxName] = clip;
            }
            else Debug.LogWarning($"[AudioManager] SFX not found: Audio/SFX/{sfxName}");
            return clip;
        }'''

if old_load in content:
    content = content.replace(old_load, new_load)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Injected CreateSpedUpClip logic into LoadSFX.")
else:
    print("Could not find the target code string.")
