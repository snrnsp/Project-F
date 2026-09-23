import codecs
import re

path = 'c:/Users/cccc0/Documents/Project-F/Assets/Scripts/UI/Theme/HalloweenUIBuilder.cs'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''            Image characterImageRight = CreateCharacterSlot("CharacterImageRight", dialoguePanelRoot.transform, 0.8f);

            // Dialogue Panel'''

replacement = '''            Image characterImageRight = CreateCharacterSlot("CharacterImageRight", dialoguePanelRoot.transform, 0.8f);

            // Flashback Overlay (between characters and dialogue panel)
            GameObject flashbackObj = UIHelper.CreateUIObject("FlashbackOverlay", dialoguePanelRoot.transform);
            UIHelper.StretchFull(flashbackObj.GetComponent<RectTransform>());
            Image flashbackImg = UIHelper.AddImage(flashbackObj, new Color32(15, 10, 25, 140)); // Dark purple semi-transparent tint
            flashbackImg.raycastTarget = false;
            flashbackObj.SetActive(false); // Off by default
            UIHelper.SetField(dialogueUi, "flashbackOverlay", flashbackObj);

            // Dialogue Panel'''

text = text.replace(target, replacement)

with open(path, 'w', encoding='utf-8-sig') as f:
    f.write(text)

print('Added FlashbackOverlay to HalloweenUIBuilder')
