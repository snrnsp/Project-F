import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

text = text.replace('FindObjectOfType<HalloweenVN.UI.Theme.ScreenTransition>()', 'FindFirstObjectByType<HalloweenVN.UI.Theme.ScreenTransition>()')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)
print("Replaced FindObjectOfType with FindFirstObjectByType")
