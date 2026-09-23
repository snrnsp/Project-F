import codecs

# Fix DialogueUI.cs
path1 = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path1, 'r', encoding='utf-8') as f:
    text1 = f.read()

text1 = text1.replace('Object.FindObjectOfType<BacklogUI>(true)', 'Object.FindFirstObjectByType<BacklogUI>(UnityEngine.FindObjectsInactive.Include)')

with open(path1, 'w', encoding='utf-8-sig') as f:
    f.write(text1)

# Fix HalloweenUIBuilder.cs
path2 = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path2, 'r', encoding='utf-8') as f:
    text2 = f.read()

text2 = text2.replace('Object.FindObjectOfType<SettingsUI>(true)', 'Object.FindFirstObjectByType<SettingsUI>(UnityEngine.FindObjectsInactive.Include)')

with open(path2, 'w', encoding='utf-8-sig') as f:
    f.write(text2)

print('Fixed obsolete method warnings')
