import re

with open('Assets/Scripts/UI/DialogueUI.cs', 'r', encoding='utf-8-sig') as f:
    content = f.read()

old_block = '''                    else
                    {
                        // Same slot: expression change only
                        StopSlotCoroutines(s);
                        LoadSpriteToImage(img, requested[s]);
                        img.gameObject.SetActive(true);
                    }'''

new_block = '''                    else
                    {
                        // Same slot: expression change only
                        StopSlotCoroutines(s);
                        LoadSpriteToImage(img, requested[s]);
                        img.gameObject.SetActive(true);
                        
                        // Force snap to prevent lingering slides from previous nodes
                        SetCharacterAnchorX(img.rectTransform, targetX[s]);
                    }'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('Assets/Scripts/UI/DialogueUI.cs', 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print("Patched DialogueUI.cs with force snap")
else:
    print("Could not find the block to patch!")
