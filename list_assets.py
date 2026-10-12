import os

path = r'F:\프로젝트 에셋\오블리비언'
for root, dirs, files in os.walk(path):
    for f in files:
        if 'LOST' in f.upper() or 'LOGO' in f.upper():
            print(os.path.join(root, f))
