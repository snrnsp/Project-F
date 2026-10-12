import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

content = content.replace('bgSprite = Sprite.Create(tex, new Rect(0, 0, tex.width, tex.height), new Vector2(0.5f, 0.5f));',
                          'bgSprite = Sprite.Create(tex, new Rect(0, 0, 1920, 1080), new Vector2(0.5f, 0.5f));')

with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("Updated Sprite.Create to use 1920x1080 explicitly.")
