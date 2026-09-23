import os
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Resources/Characters/카스미'
files = [f for f in os.listdir(path) if f.endswith('.meta')]

for f in files:
    full_path = os.path.join(path, f)
    with open(full_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace global alignment and spritePivot
    content = re.sub(r'alignment: 0\s+spritePivot: \{x: 0\.5, y: 0\.5\}', r'alignment: 9\n    spritePivot: {x: 0.43, y: 0.5}', content)
    
    # Replace per-sprite alignment and pivot
    content = re.sub(r'alignment: 0\s+pivot: \{x: 0, y: 0\}', r'alignment: 9\n        pivot: {x: 0.43, y: 0.5}', content)
    content = re.sub(r'alignment: 0\s+pivot: \{x: 0\.5, y: 0\.5\}', r'alignment: 9\n        pivot: {x: 0.43, y: 0.5}', content)
    
    with open(full_path, 'w', encoding='utf-8') as file:
        file.write(content)

print(f'Updated {len(files)} meta files.')
