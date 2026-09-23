import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = 'Texture2D triTex = new Texture2D(texSize, texSize, TextureFormat.RGBA32, false);'
replacement = '''Texture2D triTex = new Texture2D(texSize, texSize, TextureFormat.RGBA32, false);
            triTex.wrapMode = TextureWrapMode.Clamp;'''

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print('Fixed texture wrap mode for warning icon')
else:
    print('Target not found')
