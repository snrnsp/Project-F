import sys

filepath = 'F:/Project-F/Assets/Scripts/Core/GameManager.cs'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Change initial phase to Splash
content = content.replace('CurrentPhase { get; private set; } = GamePhase.Lobby;', 'CurrentPhase { get; private set; } = GamePhase.Splash;')

# GameManager doesn't have Start(). Let's add it.
start_method = '''        private void Start()
        {
            ChangePhase(GamePhase.Splash);
        }

        public void ChangePhase(GamePhase newPhase)'''

content = content.replace('public void ChangePhase(GamePhase newPhase)', start_method)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated GameManager.cs")
