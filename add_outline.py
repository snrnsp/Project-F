import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            Text lobbyTitleText = CreateLegacyText(titleObj, "오블리비언\n<size=22>OBLIVION</size>", new Color32(255, 150, 40, 255), 56, TextAnchor.MiddleCenter);
            lobbyTitleText.fontStyle = FontStyle.Bold;
            lobbyTitleText.lineSpacing = 0.65f;'''

replacement = '''            Text lobbyTitleText = CreateLegacyText(titleObj, "오블리비언\n<size=22>OBLIVION</size>", new Color32(255, 150, 40, 255), 56, TextAnchor.MiddleCenter);
            lobbyTitleText.fontStyle = FontStyle.Bold;
            lobbyTitleText.lineSpacing = 0.65f;
            Outline titleOutline = titleObj.AddComponent<Outline>();
            titleOutline.effectColor = new Color32(0, 0, 0, 255);
            titleOutline.effectDistance = new Vector2(2, -2);'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added Outline component to lobby title')
