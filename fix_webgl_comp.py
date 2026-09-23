import codecs

path = 'c:/Users/cccc0/Documents/Project-F/ProjectSettings/ProjectSettings.asset'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = 'webGLCompressionFormat: 2'
replacement = 'webGLCompressionFormat: 0'

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Disabled WebGL Compression in ProjectSettings.asset")
else:
    print("Could not find the compression setting.")
