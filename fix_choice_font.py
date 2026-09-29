import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'var choiceBtnTuple = UIHelper.CreateButton(templatesRoot, "Choice"' in line:
        new_lines.append('            choiceBtnTuple.btnText.fontSize = HalloweenTheme.ChoiceFontSize;\n')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.writelines(new_lines)
print("Choice font size mapped")
