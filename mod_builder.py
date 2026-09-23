import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Add mappings for skipButtonText and backlogButtonText
text = text.replace('UIHelper.SetField(ui, \"autoButtonText\", autoText);', 'UIHelper.SetField(ui, \"autoButtonText\", autoText);\n            UIHelper.SetField(ui, \"skipButtonText\", skipTuple.Item2);\n            UIHelper.SetField(ui, \"backlogButtonText\", logTuple.Item2);')

# Increase width of buttons so text doesn't overflow
# Currently: float btnW = 90, btnH = 35, btnSpacing = 8;
text = text.replace('float btnW = 90, btnH = 35, btnSpacing = 8;', 'float btnW = 120, btnH = 40, btnSpacing = 10;')

# Need to fix the anchors/positions if they overlap
# autoRt.anchoredPosition = new Vector2(-(btnW * 3 + btnSpacing * 2 + 10), -8);
# skipRt.anchoredPosition = new Vector2(-(btnW * 2 + btnSpacing + 10), -8);
# logRt.anchoredPosition = new Vector2(-(btnW + 10), -8);
# They are mathematically correct so they will just expand leftwards nicely.

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added skipButtonText and backlogButtonText mapping to HalloweenUIBuilder')
