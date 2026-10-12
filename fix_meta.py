import re

filepath = 'F:/Project-F/Assets/Resources/Images/Logos/LOST_STUDIO_Logo.png.meta'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Change spriteMode to 1 (Single)
content = re.sub(r'spriteMode: \d+', 'spriteMode: 1', content)

# Remove the 'sprites:' list and make it empty, or just let Unity regenerate it.
# Actually, the safest way is to just delete the meta file and let Unity recreate it as a default Single Sprite, 
# but Unity might default to Texture if it's in Resources. 
# Let's just fix spriteMode: 1 and clear the sprites array.

content = re.sub(r'(?s)    sprites:\n.*?\n    outline:', '    sprites: []\n    outline:', content)
content = re.sub(r'(?s)    nameFileIdTable:\n.*?\n  mipmapLimitGroupName:', '    nameFileIdTable: {}\n  mipmapLimitGroupName:', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated meta file.")
