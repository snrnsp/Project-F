import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('yield return new WaitForSeconds(2f);', 'yield return new WaitForSeconds(0.5f);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Reduced preview message wait time from 2s to 0.5s')
