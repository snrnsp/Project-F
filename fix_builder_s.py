import sys

path = 'F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

# I will just replace the string "2.0s" and "2s" manually
lines = content.split('\n')
new_lines = []
for line in lines:
    if 'autoPlayValueText = CreateLegacyText' in line:
        if '"2.0s"' in line:
            line = line.replace('"2.0s"', '"2.0"')
        elif '"2s"' in line:
            line = line.replace('"2s"', '"2.0"')
    new_lines.append(line)

content = '\n'.join(new_lines)
with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(content)
print("HalloweenUIBuilder initialized text updated")
