import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

with open(path, 'w', encoding='utf-8-sig') as f:
    for i, line in enumerate(lines):
        if i == 221 and line.strip() == 'private':
            continue
        f.write(line)
print("Removed stray 'private' on line 222.")
