import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/GameManager.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('if (pauseStatus && CurrentPhase != GamePhase.Lobby)', 'if (pauseStatus && CurrentPhase != GamePhase.Lobby && CurrentPhase != GamePhase.Splash)')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated OnApplicationPause in GameManager")
