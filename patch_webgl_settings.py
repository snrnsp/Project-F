import re

# Patch ProjectSettings.asset
with open('ProjectSettings/ProjectSettings.asset', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'webGLCompressionFormat: \d+', 'webGLCompressionFormat: 1', content)

with open('ProjectSettings/ProjectSettings.asset', 'w', encoding='utf-8') as f:
    f.write(content)

# Patch QualitySettings.asset
with open('ProjectSettings/QualitySettings.asset', 'r', encoding='utf-8') as f:
    qcontent = f.read()

qcontent = re.sub(r'WebGL: \d+', 'WebGL: 0', qcontent)

with open('ProjectSettings/QualitySettings.asset', 'w', encoding='utf-8') as f:
    f.write(qcontent)

print("Patched WebGL settings")
