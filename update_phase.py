import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/GamePhase.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Lobby,', 'Splash,\n        Lobby,')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated GamePhase.cs")
