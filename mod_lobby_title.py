import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('lobbyTitleText.text = "\uc624\ube14\ub9ac\ube44\uc5b8";', 'lobbyTitleText.text = "\uc624\ube14\ub9ac\ube44\uc5b8\\n<size=30>OBLIVION</size>";')
text = text.replace('lobbyTitleText.text = "\u30aa\u30d6\u30ea\u30d3\u30aa\u30f3";', 'lobbyTitleText.text = "\u30aa\u30d6\u30ea\u30d3\u30aa\u30f3\\n<size=30>OBLIVION</size>";')
text = text.replace('lobbyTitleText.text = "\u9057\u5fd8";', 'lobbyTitleText.text = "\u9057\u5fd8\\n<size=30>OBLIVION</size>";')
text = text.replace('lobbyTitleText.text = "\u907a\u5fd8";', 'lobbyTitleText.text = "\u907a\u5fd8\\n<size=30>OBLIVION</size>";')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated LobbyUI text for titles')
