import sys

# Remove _lastTextSpeed from DialogueUI.cs
filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()
content = content.replace('        private float _lastTextSpeed = -1f;\n', '')
with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)

# Remove lastSfxPreviewTime from SettingsUI.cs
filepath = 'F:/Project-F/Assets/Scripts/UI/SettingsUI.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()
content = content.replace('        private float lastSfxPreviewTime = -1f;\n', '')
with open(filepath, 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("Removed unused variables.")
