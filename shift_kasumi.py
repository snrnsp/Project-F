import glob
import re

files = glob.glob('c:/Users/cccc0/Documents/Project-F/Assets/Resources/Characters/카스미/*.meta')
count = 0

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to change the pivot x to 0.38
    new_content = re.sub(r'(alignment:\s*9\s*\n\s*pivot:\s*\{x:\s*)0\.[0-9]+(,\s*y:\s*0\.5\})', r'\g<1>0.38\g<2>', content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f'Updated {count} meta files for Kasumi.')
