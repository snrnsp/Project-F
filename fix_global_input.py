import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/GlobalUIManager.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Add using UnityEngine.InputSystem
if 'using UnityEngine.InputSystem;' not in text:
    text = text.replace('using UnityEngine;', 'using UnityEngine;\nusing UnityEngine.InputSystem;')

# Replace Input.GetKeyDown(KeyCode.Escape)
text = text.replace('if (Input.GetKeyDown(KeyCode.Escape))', 'if (Keyboard.current != null && Keyboard.current.escapeKey.wasPressedThisFrame)')

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated GlobalUIManager.cs')
