import codecs

# Fix LobbyUI.cs
path1 = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path1, 'r', encoding='utf-8') as f:
    text1 = f.read()

text1 = text1.replace('extraText.text = "\uc5d1\uc2a4\ud2b8\ub77c";', 'extraText.text = "\uce90\ub9ad\ud130";')
text1 = text1.replace('extraText.text = "Extra";', 'extraText.text = "Character";')
text1 = text1.replace('extraText.text = "\u304a\u307e\u3051";', 'extraText.text = "\u30ad\u30e3\u30e9\u30af\u30bf\u30fc";')
text1 = text1.replace('extraText.text = "\u989d\u5916\u5185\u5bb9";', 'extraText.text = "\u89d2\u8272";')

with open(path1, 'w', encoding='utf-8-sig') as f:
    f.write(text1)

# Fix HalloweenUIBuilder.cs
path2 = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path2, 'r', encoding='utf-8') as f:
    text2 = f.read()

text2 = text2.replace('CreateLegacyButton(lobbyPanelRoot.transform, "\uc5d1\uc2a4\ud2b8\ub77c",', 'CreateLegacyButton(lobbyPanelRoot.transform, "\uce90\ub9ad\ud130",')

with open(path2, 'w', encoding='utf-8-sig') as f:
    f.write(text2)

print('Changed Extra button text to Character')
