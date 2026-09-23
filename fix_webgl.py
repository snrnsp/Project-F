import codecs

path = 'c:/Users/cccc0/Documents/Project-F/ProjectSettings/ProjectSettings.asset'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = 'webGLDecompressionFallback: 0'
replacement = 'webGLDecompressionFallback: 1'

if target in text:
    text = text.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed Decompression Fallback in ProjectSettings.asset")
else:
    print("Could not find the setting.")
