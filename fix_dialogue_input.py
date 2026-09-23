import codecs

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Add using UnityEngine.InputSystem
if 'using UnityEngine.InputSystem;' not in text:
    text = text.replace('using UnityEngine;', 'using UnityEngine;\nusing UnityEngine.InputSystem;')

# 1. Right click
text = text.replace('if (Input.GetMouseButtonDown(1))', 'if (Mouse.current != null && Mouse.current.rightButton.wasPressedThisFrame)')

# 2. Left click or Space or Enter
target_2 = 'if (Input.GetMouseButtonDown(0) || Input.GetKeyDown(KeyCode.Space) || Input.GetKeyDown(KeyCode.Return))'
replacement_2 = 'if ((Mouse.current != null && Mouse.current.leftButton.wasPressedThisFrame) || (Keyboard.current != null && Keyboard.current.spaceKey.wasPressedThisFrame) || (Keyboard.current != null && Keyboard.current.enterKey.wasPressedThisFrame))'
text = text.replace(target_2, replacement_2)

# 3. Mouse Scroll Up
target_3 = 'if (Input.mouseScrollDelta.y > 0)'
replacement_3 = 'if (Mouse.current != null && Mouse.current.scroll.ReadValue().y > 0)'
text = text.replace(target_3, replacement_3)

# 4. Space / Enter
target_4 = 'if (Input.GetKeyDown(KeyCode.Space) || Input.GetKeyDown(KeyCode.Return))'
replacement_4 = 'if ((Keyboard.current != null && Keyboard.current.spaceKey.wasPressedThisFrame) || (Keyboard.current != null && Keyboard.current.enterKey.wasPressedThisFrame))'
text = text.replace(target_4, replacement_4)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Updated DialogueUI.cs')
