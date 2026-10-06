import os
import re

count = 0
for root, dirs, files in os.walk('Assets/Resources'):
    for file in files:
        if file.endswith('.png.meta') or file.endswith('.jpg.meta'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Enable crunch compression globally for the texture
            if 'crunchedCompression: 0' in content:
                content = content.replace('crunchedCompression: 0', 'crunchedCompression: 1')
                content = content.replace('textureCompression: 1', 'textureCompression: 2') # 2 is Crunch
                
            # Add WebGL override if missing, or edit if present
            webgl_block = '''  - serializedVersion: 3
    buildTarget: WebGL
    maxTextureSize: 1024
    resizeAlgorithm: 0
    textureFormat: 12
    textureCompression: 2
    compressionQuality: 50
    crunchedCompression: 1
    allowsAlphaSplitting: 0
    overridden: 1
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0'''

            if 'buildTarget: WebGL' not in content:
                # Find platformSettings: and append
                if 'platformSettings:\n' in content:
                    content = content.replace('platformSettings:\n', 'platformSettings:\n' + webgl_block + '\n')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1

print(f"Patched {count} image meta files for WebGL compression.")
