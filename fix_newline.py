import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    text = f.read()

target = "'에 있습니다!\n\n게임의 품질이 낮을 수 있는 점 양해 바랍니다!\";"
replacement = "'에 있습니다!\\n\\n게임의 품질이 낮을 수 있는 점 양해 바랍니다!\";"
# Or just replacing the exact strings based on what was found:
# Wait, let's just do a string replace for the specific lines.

target_raw = "에 있습니다!\n\n게임의"
replacement_raw = "에 있습니다!\\n\\n게임의"

if target_raw in text:
    text = text.replace(target_raw, replacement_raw)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(text)
    print("Fixed newline in constant.")
else:
    print("Target not found.")
