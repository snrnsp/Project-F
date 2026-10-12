import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/AudioManager.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = '''        public void PlaySFX(string sfxName, float maxDuration = 0f, float fadeOutTime = 1f)
        {
            AudioClip clip = LoadSFX(sfxName);'''

new_code = '''        public void PlaySFX(string sfxName, float maxDuration = 0f, float fadeOutTime = 1f)
        {
            Debug.Log("[AudioManager] PlaySFX called with: " + sfxName);
            AudioClip clip = LoadSFX(sfxName);'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Added Debug.Log to PlaySFX.")
else:
    print("Could not find the target code string.")
