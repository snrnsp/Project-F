import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/ExtraUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = '''                    if (i < folderTabImages.Count && folderTabImages[i] != null)
                        folderTabImages[i].color = selectedFolderColor;'''

rep = '''                    if (i < folderTabImages.Count && folderTabImages[i] != null)
                        folderTabImages[i].color = selectedFolderColor;
                    
                    Image seamImg = folder.transform.Find("TabContainer/Seam")?.GetComponent<Image>();
                    if (seamImg != null) seamImg.color = selectedFolderColor;'''

target2 = '''                    if (i < folderTabImages.Count && folderTabImages[i] != null)
                        folderTabImages[i].color = unselectedTabColor;'''

rep2 = '''                    if (i < folderTabImages.Count && folderTabImages[i] != null)
                        folderTabImages[i].color = unselectedTabColor;
                    
                    Image seamImg = folder.transform.Find("TabContainer/Seam")?.GetComponent<Image>();
                    if (seamImg != null) seamImg.color = unselectedTabColor;'''

text = text.replace(target, rep).replace(target2, rep2)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated ExtraUI to support dynamic seam coloring')
