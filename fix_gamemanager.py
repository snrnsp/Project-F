import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/GameManager.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

bad_line = 'ChangePhase(GamePhase.Splash);'
good_line = 'ChangePhase(GamePhase.Lobby);'
content = content.replace(bad_line, good_line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed GameManager.Start() race condition!")
