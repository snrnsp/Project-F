import sys
sys.stdout.reconfigure(encoding='utf-8')

# Fix ExtraUI.cs
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

text = text.replace('folderTabTexts[i].fontSize = 65;', 'folderTabTexts[i].fontSize = 55;')
# Now find the one that was originally 55 (unselected)
# Since I already changed 65 to 55, I should have done 55 first.
# Let's just read again
with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

text = text.replace('folderTabTexts[i].fontSize = 55;', 'folderTabTexts[i].fontSize = 45;')
text = text.replace('folderTabTexts[i].fontSize = 65;', 'folderTabTexts[i].fontSize = 55;')

with open('F:/Project-F/Assets/Scripts/UI/ExtraUI.cs', 'w', encoding='utf-8-sig') as f:
    f.write(text)

# Fix HalloweenUIBuilder.cs
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text2 = f.read()

text2 = text2.replace('Color.black, 65, TextAlignmentOptions.Center', 'Color.black, 55, TextAlignmentOptions.Center')

with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
    f.write(text2)

print('Font sizes reduced to 55/45')
