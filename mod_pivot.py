import os
import re

base_path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Characters'
names = ['\ubbf8\ub098', '\ud558\ub8e8\uce74'] # 미나, 하루카

for name in names:
    dir_path = os.path.join(base_path, name)
    if not os.path.exists(dir_path):
        continue
    
    for filename in os.listdir(dir_path):
        if filename.endswith('.png.meta'):
            file_path = os.path.join(dir_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = re.sub(r'spritePivot: \{x: 0\.5, y: 0\.5\}', 'spritePivot: {x: 0.43, y: 0.5}', content)
            content = re.sub(r'pivot: \{x: 0\.5, y: 0\.5\}', 'pivot: {x: 0.43, y: 0.5}', content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

print('Updated pivot for Mina and Haruka sprites')
