import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/AudioManager.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = '''                    tempSource.pitch = 2.0f;
                    tempSource.spatialBlend = 0f;
                    tempSource.Play();'''

new_code = '''                    tempSource.pitch = 2.0f;
                    tempSource.spatialBlend = 0f;
                    tempSource.Play();
                    Debug.Log("[AudioManager] Played UI SFX at 2x pitch!");'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Added Debug.Log.")
else:
    print("Could not find the target code string.")
