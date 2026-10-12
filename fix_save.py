import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/GameManager.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('if (CurrentPhase != GamePhase.Lobby)', 'if (CurrentPhase != GamePhase.Lobby && CurrentPhase != GamePhase.Splash)')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated GameManager.cs to prevent saving in Splash phase")
