import codecs

filepath = 'F:/Project-F/Assets/Scripts/UI/LobbyUI.cs'
with codecs.open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

target = 'private void Start()\r\n        {\r\n'
replacement = 'private void Start()\r\n        {\r\n            ShowPreAlphaWarning();\r\n'

if target in content:
    content = content.replace(target, replacement)
    print("Injected successfully with \\r\\n")
else:
    target2 = 'private void Start()\n        {\n'
    replacement2 = 'private void Start()\n        {\n            ShowPreAlphaWarning();\n'
    if target2 in content:
        content = content.replace(target2, replacement2)
        print("Injected successfully with \\n")
    else:
        print("Could not find Start() signature")

with codecs.open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)
