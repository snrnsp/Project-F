import os

path = r'F:\프로젝트 에셋\오블리비언'
with open('logo_files.txt', 'w', encoding='utf-8') as out:
    for root, dirs, files in os.walk(path):
        for f in files:
            if 'LOST' in f.upper() or 'LOGO' in f.upper() or '로고' in f:
                out.write(os.path.join(root, f) + '\n')
