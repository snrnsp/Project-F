import sys

filepath = 'F:/Project-F/Assets/Scripts/UI/DialogueUI.cs'
with open(filepath, 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_code = '''                // ADDED: 0.1-second delay check after typing is finished
                if (Time.unscaledTime - _typingEndTime < 0.1f)
                {
                    Debug.Log($"[DialogueUI] Advance ignored due to 0.1-second cooldown.");
                    return;
                }'''

if old_code in content:
    content = content.replace(old_code, "")
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Removed 0.1s typing delay cooldown.")
else:
    print("Could not find the target code string.")
