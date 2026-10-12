import os
import re

def check_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith('.cs'): continue
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    content = f.read()
                except:
                    with open(filepath, 'r', encoding='utf-8-sig') as f2:
                        content = f2.read()
            
            # Find methods
            update_blocks = re.finditer(r'void\s+Update\s*\(\)\s*\{', content)
            for m in update_blocks:
                start = m.end()
                open_braces = 1
                i = start
                while i < len(content) and open_braces > 0:
                    if content[i] == '{': open_braces += 1
                    elif content[i] == '}': open_braces -= 1
                    i += 1
                update_content = content[start:i]
                if 'FindObject' in update_content or 'FindGameObject' in update_content or 'Camera.main' in update_content:
                    print(f"Warning: Expensive call in Update of {file}")
            
            # Check AddListener without RemoveListener
            adds = len(re.findall(r'\.AddListener\(', content))
            removes = len(re.findall(r'\.RemoveListener\(', content))
            if adds > removes and ('OnEnable' in content or 'Start' in content):
                # Could be anonymous lambdas, check if there are any non-lambda AddListeners
                pass
                
check_files('F:/Project-F/Assets/Scripts')
print('Done.')
