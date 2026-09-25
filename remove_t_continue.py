import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'r', encoding='utf-8-sig') as f:
    text = f.read()

text = re.sub(r'[ \t]*string t_continue = "[^"]+";\r?\n', '', text)

with open('F:/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs', 'w', encoding='utf-8-sig') as f:
    f.write(text)
print('Variable t_continue removed')
