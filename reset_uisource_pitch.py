import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/AudioManager.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace('uiSource.pitch = 2.0f; // Double speed for UI sounds', 'uiSource.pitch = 1.0f; // Default pitch')

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Reset uiSource pitch to 1.0f.")
