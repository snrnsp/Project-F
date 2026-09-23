import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Make portrait smaller
text = text.replace('portraitRt.offsetMin = new Vector2(40, 50);', 'portraitRt.offsetMin = new Vector2(80, 120);')
text = text.replace('portraitRt.offsetMax = new Vector2(-20, -180);', 'portraitRt.offsetMax = new Vector2(-60, -260);')

# Increase margins for text (info panel)
text = text.replace('nameText.margin = new Vector4(15, 10, 15, 0);', 'nameText.margin = new Vector4(40, 20, 40, 0);')
text = text.replace('profileText.margin = new Vector4(15, 5, 15, 15);', 'profileText.margin = new Vector4(40, 10, 40, 40);')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Adjusted Extra UI layout')
