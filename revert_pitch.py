import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/AudioManager.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = 'tempSource.pitch = 3.0f;'
new_code = 'tempSource.pitch = 2.0f;'

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Reverted pitch back to 2.0f.")
else:
    print("Could not find the target code string.")
