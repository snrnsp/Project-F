import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/LobbyUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

# Also ensure I add if(continueText != null) to UpdateContinueButton if needed?
# Let's check UpdateContinueButton first.

text = re.sub(r'[ \t]*continueText\.text = "[^"]+";\r?\n', '', text)

with open('F:/Project-F/Assets/Scripts/UI/LobbyUI.cs', 'w', encoding='utf-8-sig') as f:
    f.write(text)
print('continueText assignments removed from LobbyUI.cs')
