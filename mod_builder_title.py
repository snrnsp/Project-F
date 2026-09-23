import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('CreateLegacyText(titleObj, "\uc624\ube14\ub9ac\ube44\uc5b8", ', 'CreateLegacyText(titleObj, "\uc624\ube14\ub9ac\ube44\uc5b8\\n<size=30>OBLIVION</size>", ')
# Increase sizeDelta just in case
text = text.replace('titleRt.sizeDelta = new Vector2(400, 80);', 'titleRt.sizeDelta = new Vector2(400, 120);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated initial title in HalloweenUIBuilder')
