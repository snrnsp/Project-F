import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/AudioManager.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = '''            if (uiSource == null)
            {
                uiSource = gameObject.AddComponent<AudioSource>();
                uiSource.loop = false;
                uiSource.playOnAwake = false;
                uiSource.spatialBlend = 0f;
                uiSource.pitch = 2.0f; // Double speed for UI sounds
            }'''

new_code = '''            if (uiSource == null)
            {
                uiSource = gameObject.AddComponent<AudioSource>();
                uiSource.loop = false;
                uiSource.playOnAwake = false;
                uiSource.spatialBlend = 0f;
            }
            uiSource.pitch = 2.0f; // Double speed for UI sounds'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Fixed uiSource pitch.")
else:
    print("Could not find the target code string.")
