import re

with open('Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

# Fix the 'from == s' block to also stop coroutines and ensure the object is active
old_block = '''                    else
                    {
                        // Same slot: expression change only
                        LoadSpriteToImage(img, requested[s]);
                    }'''

new_block = '''                    else
                    {
                        // Same slot: expression change only
                        StopSlotCoroutines(s);
                        LoadSpriteToImage(img, requested[s]);
                        img.gameObject.SetActive(true);
                    }'''

content = content.replace(old_block, new_block)

with open('Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
    f.write(content)

print("Patched DialogueUI.cs")
